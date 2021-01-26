while true; do
    read -p "Are you in a virtualenv? (y/n) : " yn
    case $yn in
        [Yy]* ) echo "starting build"; break;;
        [Nn]* ) echo "please start a virtualenv and try again ...";exit;;
        * ) echo "Please answer yes or no.";;
    esac
done

cd ui;
npm run buildcp;
cd ..
python3 -m pip install -r requirements.txt

printf "\n  you can start the app with \n    python3 manage.py runserver \n\n  then open: \n    http://localhost:8000/static/index.html \n  in the browser. \n\n\n"