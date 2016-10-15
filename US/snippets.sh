# restart all US windows, copy pdbs from old folder
cp --parents -R windows-withMin/**/**/*.pdb ./windows/

# in the directory to be completely restarted, clean files, leaving inputs and scripts:
find . -maxdepth 1 -type f ! \( -iname '*.inp' -o -iname '*.pbs' -o -iname '*.sh' -o -iname '*.pdb' \) -delete
