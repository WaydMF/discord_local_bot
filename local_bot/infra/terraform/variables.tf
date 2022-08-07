variable "account_id" {
  type = number
}

variable "dynamodb_table_name" {
  type = string
}

variable "service" {
  default = "Local Bot"
  type    = string
}

variable "project" {
  default = "local-bot"
  type    = string
}

variable "region" {
  default = "eu-west-2"
  type    = string
}
