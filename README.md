# Terraform 

Provisions the GCS data lake bucket and BigQuery dataset for the semiconductor industry data pipeline.

## Resources

- `google_storage_bucket.semiconductor_data_lake` — GCS bucket (uniform bucket-level access enabled)
- `google_bigquery_dataset.semiconductor_dataset` — BigQuery dataset

## Usage

```sh
cp terraform.tfvars.example terraform.tfvars   # fill in your project/values
terraform init
terraform plan
terraform apply
```
