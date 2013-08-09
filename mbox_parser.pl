use Config::Simple;
use Data::Dumper;
use Net::IMAP::Simple::SSL;
use Email::Simple;
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
 

sub get_employee_id {
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
 
$imap->login($user => $pass) || die "Unable to logini $user/$pass\n";
  
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
				print "Found hashtag line : [$line}\n";
				while($line =~/#(\w+)/g){
					print "Found Hashtag $1\n";
					$hashtags.="$1,";
				}
			}
		}
	
		my @addrs = Mail::Address->parse($es->header('To'));
	 	foreach $addr (@addrs) {
	     		print " --> ".$addr->format,"\n";
	    	 	if( $addr->format=~/([a-z\.]+)\@tubemogul.com/ ){
				$to_id=get_employee_id($dbh,$1);
		  		$dbh->do("insert into kudosapp_kudos (from_employee_id, to_employee_id, created, subject, body, tags) values ($from_id, $to_id, NOW(), '".$es->header('Subject')."', '<>', '$hashtags')");
	     		} else {
				die "Failed to parse :(\n";
	     		}
	
	 	}
	} else { 
		print "Skipped, not the first mail of the thread\n";
	}

}
$imap->quit;
