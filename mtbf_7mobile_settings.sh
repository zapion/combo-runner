unzip gaia.zip

cd gaia/profile/webapps/settings.gaiamobile.org/
mkdir application
cd application
cp ../application.zip .
unzip application.zip
rm -rf applcation.zip
cp /mnt/mtbf_shared/resources/apn.json shared/resources/
zip -r application.zip *
cp application.zip ../
cd ..
rm -rf application

cd ../system.gaiamobile.org/
mkdir application
cd application
cp ../application.zip .
unzip application.zip
rm -rf applcation.zip
cp /mnt/mtbf_shared/resources/apn.json shared/resources/
zip -r application.zip *
cp application.zip ../
cd ..
rm -rf application

cd ../../../../
rm -rf gaia.zip
zip -r gaia.zip gaia/
rm -rf gaia
