#!/usr/bin/perl -w

use strict;

# grok the easy hacks data into something fun

my $fh;
my $date = '';
my @changes = ();
print "Lines\n";
open ($fh, "git log --numstat unusedcode.easy|") || die "Can't git log: $!";
while (<$fh>) {
#    print "$_";
    if (/^Date:\s*(.*)$/) {
	$date = $1;
    } elsif (/^(\d+)\s+(\d+)\s+/) {
	my %change;
	$change{plus} = $1;
	$change{minus} = $2;
#	$change{date} = $date;
	push @changes, \%change;
	my $rec = \%change;
    }
}
close ($fh);

my $number = 0;
for my $rec (reverse (@changes)) {
    $number = $number + $rec->{plus} - $rec->{minus};
#    print "+$rec->{plus} - $rec->{minus}\n";
    print "$number\n";
}
