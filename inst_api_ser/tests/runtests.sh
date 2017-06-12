python test_main.py ../reports/tests.html

if grep -q "class='failClass'" ../reports/tests.html; then
    rsync -avzh -e ssh ../reports server@192.168.0.96:./development/projects/insights
    exit 64
else
	if grep -q "class='errorClass'" ../reports/tests.html; then
    	rsync -avzh -e ssh ../reports server@192.168.0.96:./development/projects/insights
    	exit 64
    fi
    rsync -avzh -e ssh ../reports server@192.168.0.96:./development/projects/insights
    exit 0
fi