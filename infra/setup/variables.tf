variable "tf_state_bucket" {
  description = "Name of S3 bucket in AWS for storing TF state"
  default     = "devops-propertydeck-tf-state"
}

variable "tf_state_lock_table" {
  description = "Name of the DynamoDB table for TF state locking"
  default     = "devops-property-"
}

variable "project" {
  description = "Project for tagging resource"
  default     = "property-app-api"
}

variable "contact" {
  description = "Contact name for tagging resources"
  default     = "saisudhagadre1999@gmail.com"
}
