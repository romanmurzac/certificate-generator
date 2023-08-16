# Certificate Generator

## Description
The project contains a service that helps to generate a certificate with personal data.

It will be used at the end of the course as proof of successful completion of the retraining program. Also, it will be used by recruiters and TSLs.

### Requirements
Requirements are in the Confluence location: https://confluence.softserveinc.com/pages/viewpage.action?spaceKey=BDACD&title=Certificate+generator

### Input
- Student name
- Title of the Retraining Program
- Status
- Date

### Output
- PNG image as a custom certificate

## Working mode

### Initial
The default link with template of the certificate: https://europe-central2-gcp101167-competencedevelopmen.cloudfunctions.net/certificate_generator

### Working stages
- start from the link provided on *Initial* step
- add the *student_name* by separating the last name from the first name with a whitespace.
- add the *title* of the Retraining Program by separating the words with a whitespace.
- add the *status* of the completion - "successfully completed" or "completed".
- add the *date* of the Certificate issue in follow format: **22.03.2023**.

### Result
The custom certificate with specific student data: https://europe-central2-gcp101167-competencedevelopmen.cloudfunctions.net/certificate_generator?student_name=kateryna%20yatsenko&title=bi%20retraining%20program%20for%20big%20data&status=successfully%20completed&date=22.03.2023


## Repository content
- ***main.py*** - The Python file that contain the code to be deployed on Google Cloud Function
- ***requirements.txt*** - The necessary packages to be installed
- ***template_certificate.png*** - The PNG file that contains the Certificate template to be used for certificare generation
- ***proxima-nova-black.otf*** - The main font file to be used for text that is applied on certificates
- ***open-sans-regular.ttf*** - The secondary font file to be used for text that is applied on certificates
- ***README.md*** - The explanation file for the whole repository