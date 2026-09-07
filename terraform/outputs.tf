output "gcs_bucket_name" {
  description = "Name of the Google Cloud Storage data lake bucket"
  value       = google_storage_bucket.semiconductor_data_lake.name
}

output "bigquery_dataset_id" {
  description = "ID of the BigQuery dataset"
  value       = google_bigquery_dataset.semiconductor_dataset.dataset_id
}
