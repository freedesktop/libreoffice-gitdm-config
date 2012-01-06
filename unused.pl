#!/usr/bin/perl -w

use strict;
use DateTime::Format::Strptime;

# grok the easy hacks data into something fun

my $fh;
my $date = '';
my @changes = ();
my $timeparser = DateTime::Format::Strptime->new( pattern => '%a %b %d %H:%M:%S %Y' );

print "Date\tLines\n";
open ($fh, "git log --numstat unusedcode.easy|") || die "Can't git log: $!";
while (<$fh>) {
#    print "$_";
    if (/^Date:\s*(.*)\+(\d+)\s*$/) {
	$date = $1;
    } elsif (/^(\d+)\s+(\d+)\s+/) {
	my %change;
	$change{plus} = $1;
	$change{minus} = $2;
	$change{date} = $timeparser->parse_datetime($date);
	push @changes, \%change;
	my $rec = \%change;
    }
}
close ($fh);

my $number = 0;
for my $rec (reverse (@changes)) {
    $number = $number + $rec->{plus} - $rec->{minus};
#    print "+$rec->{plus} - $rec->{minus}\n";
    print $rec->{date}->date() . "\t$number\n";
}
