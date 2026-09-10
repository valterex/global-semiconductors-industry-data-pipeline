variable "project" {
  description = "GCP Project ID"
  type        = string
}

variable "region" {
  description = "GCP region for compute resources"
  type        = string
  default     = "europe-west1"
}

variable "zone" {
  description = "GCP zone for compute resources"
  type        = string
  default     = "europe-west1-b"
}

variable "location" {
  description = "GCP location for the bucket and dataset"
  type        = string
  default     = "EU"
}

variable "gcs_bucket_name" {
  description = "GCS bucket name (must be globally unique)"
  type        = string
}

variable "gcs_storage_class" {
  description = "GCS storage class"
  type        = string
  default     = "STANDARD"
}

variable "bq_dataset_name" {
  description = "BigQuery dataset name"
  type        = string
  default     = "global_semiconductor_industry"
}
