variable "project" {
  description = "GCP Project ID"
  type        = string
}

variable "region" {
  description = "Region"
  type        = string
  default     = "europe-west1"
}

variable "zone" {
  description = "Zone"
  type        = string
  default     = "europe-west1-b"
}

variable "location" {
  description = "Project Location (for bucket and dataset)"
  type        = string
  default     = "EU"
}

variable "gcs_bucket_name" {
  description = "GCS bucket name (must be globally unique)"
  type        = string
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  type        = string
  default     = "STANDARD"
}

variable "bq_dataset_name" {
  description = "BigQuery Dataset Name"
  type        = string
  default     = "global_semiconductor_industry"
}
