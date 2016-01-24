#!/bin/sh

run_stats ()
{
    mr_config=$1
    topic=${mr_config#mr-}
    topic=${topic%.config}
    output_dir=`pwd`/stats-$topic-`date -u +'%Y-%m-%d'`

	-d $output_dir || mkdir $output_dir || exit 1

	# update/clone repos
	./mr -c $mr_config update

	# warning: though the -M option is yielding more accurate stats, if you
	# need strictly backwards-comparable results, leave it out!
	./mr -c $mr_config log -p -M --since='Jan 1 19:00:00 2013' | ../gitdm/gitdm -u -X '\.(sdf|po|dic)\$' -b . -x $output_dir/git-hackers-data.csv -o $output_dir/git-hackers-reports.txt -H $output_dir/hackers.csv || exit 1

	# fudge unknown affiliations
	for item in $output_dir/git-hackers-data.csv $output_dir/hackers.csv; do
		sed -i.bak 's/(Unknown)/Assigned/' $item || exit 1
	done
}

# run all known stats
#for item in mr-*.config; do
for item in mr-legacydev.config; do
	run_stats $item
done
