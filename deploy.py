import os
import boto3

def deploy_cfn_stack(stack_name: str, template_path: str, params: dict):
  client_cfn = boto3.client('cloudformation')
  with open(template_path, 'r') as template_file:
    template_body = template_file.read()
    response = client_cfn.create_stack(
        StackName=stack_name,
        TemplateBody=template_body,
        Parameters=params,
        Capabilities=['CAPABILITY_NAMED_IAM']
    )
    print(f"Stack deployment initiated: {response}")

def upload_file_to_s3(bucket_name: str, script_parent_path: str):
  client_s3 = boto3.client('s3')
  for script in os.listdir(script_parent_path):
    script_file_path = os.path.join(script_parent_path, script)
    client_s3.upload_file(script_file_path, bucket_name, f'glue-scripts/{script}') 
    print(f"Uploaded {script} to S3")

def deploy_cfn_templates():
  deploy_cfn_stack('stack-glue-res', './cfn-templates/glue-res.yml', [{'ParameterKey': 'stack-name', 'ParameterValue': 'stack-res'}])
  deploy_cfn_stack('stack-iam-roles', './cfn-templates/iam-roles.yml', [{'ParameterKey': 'stack-name', 'ParameterValue': 'stack-iam-roles'}])

def deploy_py_scripts():
  upload_file_to_s3('bucket_py_scripts', './scripts/')

def deploy_csv():
  upload_file_to_s3('bucket_emp_data', './data/')

if __name__ == '__main__':
  deploy_cfn_templates()
  deploy_py_scripts()
  deploy_csv()