use Config::Simple;
use Data::Dumper;
use Net::IMAP::Simple::SSL;
use Email::Simple;
use Email::Send;
use Mail::Address;
use DBI;
use HTML::Entities;

$cfg = new Config::Simple('app.ini');
$host = $cfg->param('host');
$user = $cfg->param('user');
$pass = $cfg->param('pass');

$db_name = $cfg->param('db_name');
$db_user = $cfg->param('db_user');
$db_pass = $cfg->param('db_pass');
$db_host = $cfg->param('db_host');
$db_port = $cfg->param('db_port');

$dsn = "DBI:mysql:database=$db_name;host=$db_host;port=$db_port";

$dbh = DBI->connect($dsn, $db_user, $db_pass);

my $imap = Net::IMAP::Simple::SSL->new($host) || die "Unable to connect to IMAP: $Net::IMAP::Simple::errstr\n";
 

sub get_employee_id ($$) {
	my ($dbh,$e_name)=@_;
	my $sth = $dbh->prepare("SELECT id,email FROM kudosapp_employee where email='$e_name\@tubemogul.com'");
	$sth->execute();
	# FIXME : check for unicity of results
	while (my $ref = $sth->fetchrow_hashref()) {
		$to_id=$ref->{'id'};
	}
	$sth->finish();
	return $to_id;
}
 
sub is_kudo_unique ($$$){
	my ($dbh,$message_id,$to)=@_;
	my $sth = $dbh->prepare("SELECT id,message_id FROM kudosapp_kudos where message_id='$message_id' and to_employee_id='$to'");
	$sth->execute();
	$count=$sth->rows;
	$sth->finish();
	return $count==0;
}
  
 
$imap->login($user => $pass) || die "Unable to login $user/$pass\n";
  
    my $nm = $imap->select('INBOX');

    for(my $i = 1; $i <= $nm; $i++){
        if($imap->seen($i)){
            print "*";
        } else {
            print " ";
        }

        my $es = Email::Simple->new(join '', @{ $imap->top($i) } );

        printf("[%03d] %s\n", $i, $es->header('Subject'));
	
		if($es->header('In-Reply-To') eq ""){
		
			print  $es->header('From')."\n";
		    	if( $es->header('From')=~/([a-z\.]+)\@tubemogul.com/ ){
				$from_id=get_employee_id($dbh,$1);
			}
		
		
			my @message_lines = $imap->get( $i ) or die $imap->errstr;
			my $hashtags="";
			foreach $line (@message_lines) {
				if ($line=~/\+kudo/i && $line !~/=/ ) {
					# print "Found hashtag line : [$line}\n";
					while($line =~/#(\w+)/g){
						# print "Found Hashtag $1\n";
						$hashtags.="$1,";
					}
				}
			}
		
			my @addrs = Mail::Address->parse($es->header('To'));
			
			my $message = $imap->get( $i ) or die $imap->errstr;
			
			if( $message=~/Content-Type: text\/plain.+?\n(.+)Content-Type: text\/html/s ) {
				$filtered_body=$1;
			}
			
			print "Found ".scalar(@addrs)." to: \n";
			
		 	foreach $addr (@addrs) {
		     	print " --> ".$addr->format,"\n";
		    	 if( $addr->format=~/([a-z\.]+)\@tubemogul.com/ ){
					$to_id=get_employee_id($dbh,$1);
					if(is_kudo_unique($dbh,$es->header('Message-ID'),$to_id) && $to_id != $from_id){
			  			$dbh->do("insert into kudosapp_kudos 
							(from_employee_id, to_employee_id, created, subject, body, tags, message_id) values 
							($from_id, $to_id, NOW(), '".$es->header('Subject')."', '$filtered_body', '$hashtags', '".$es->header('Message-ID')."')");
					}
	     		} else {
					die "Failed to parse :(\n";
	     		}
		 	}
		} else { 
			print "Skipped, not the first mail of the thread\n";
			
			$body="
Dear Moguler,

You seemed to have kept kudos@tubemogul.com cc'd to this email thread. Please note that any replies to this thread will not register as any new kudos.

Thank you,
The Kudo Team";

			my $mailer = Email::Send->new( {
			    mailer => 'SMTP::TLS',
			    mailer_args => [
			        Host => 'smtp.gmail.com',
			        Port => 587,
			        User => $user,
			        Password => $pass,
			    ]
			} );
			
			use Email::Simple::Creator; # or other Email::
			my $email = Email::Simple->create(
			    header => [
			        From    => $user,
			        To      => $es->header('From'),
			        Subject => 'Kudos : Woops!',
			    ],
			    body => $body,
			);
			
			eval { $mailer->send($email) };	
			die "Error sending email: $@" if $@;
			print "Mail sent to ".$es->header('From')."\n";		
			
		}

}

system("/usr/bin/python /var/www/TMKudos/kudos/manage.py update_index");
$imap->quit;
