# Student_Reg_Form

## Cloud Computing Project
### Work Flow :
- Create a EC2 Server
- Ansible to create script for ec2server
- Host reg form web app on ec2 


### Ansible playbook for EC2 Launch:

- task.yml is the ansible script here to create EC2 instance. 
- Run the below command to check whether Ansible is ready to launch EC2 or not.

> ansible-playbook -C task.yml

Where -C will check if everything is ready or not.
Now, run the below command and the EC2 server will be launched.

> ansible-playbook task.yml

- Now if you go to the Amazon console you will see the server is launched successfully.
We are done with creating a basic EC2 server using Ansible.


### Application on AWS Cloud:


We use the below command to get the local version of the repository from a remote:

> git clone https://github.com/tanya-ranjan2/Student_Reg_Form.git

Now our application repository with the code is on the EC2 instance. We will create a virtual environment and then all the required libraries are installed using the below command :

> cd Student_Reg_Form/FlaskCRUDApplication2

#### Create a virtual environment
> virtualenv venv 
#### Activate the virtual environment venv
> source venv/bin/activate
#### Install the libraries stored in requirement.txt

> pip3 install -r requirement.txt

Now we are ready to run the application and host it on AWS cloud, which is by the below command:

> python3 regpage.py

Through this, our application starts on AWS and we will now set some security groups on for the EC2 instance to get the public IP accessible from everywhere. 
As our flask application is using port 5000, we make a rule for port 5000 accessible from anywhere in the security group.




