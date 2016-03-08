#!/bin/sh

run_stats ()
{
    mr_config=$1
	month=$2
    topic=${mr_config#mr-}
    topic=${topic%.config}
	echo $month
    output_dir=`pwd`/stats-$topic-$month-`date -u +'%Y-%m-%d'`

	test -d $output_dir || mkdir $output_dir || exit 1

	# warning: though the -M option is yielding more accurate stats, if you
	# need strictly backwards-comparable results, leave it out!
	./mr -c $mr_config log -p -M --since=`date -d "$month month" "+%Y-%m-01"` --before=`date -d "$((month+1)) month" "+%Y-%m-01"` | ../gitdm/gitdm -u -X '\.(sdf|po|dic)\$' -b . -x $output_dir/git-hackers-data.csv -o $output_dir/git-hackers-reports.txt -H $output_dir/hackers.csv || exit 1

	# fudge unknown affiliations
	for mangle_file in $output_dir/git-hackers-data.csv $output_dir/hackers.csv; do
		sed -i.bak 's/(Unknown)/Assigned/' $mangle_file || exit 1
	done
}

# run all known stats
for item in mr-*.config; do
	# update/clone repos
	./mr -c $item update

    for month in -1 -2 -3 -4 -5 -6; do
	    run_stats $item $month
	done
done
