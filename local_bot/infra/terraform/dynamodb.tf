resource "aws_dynamodb_table" "discord_bot_guild_config_table" {
  name           = var.dynamodb_table_name
  billing_mode   = "PROVISIONED"
  read_capacity  = 5
  write_capacity = 5
  hash_key       = "GuildID"

  attribute {
    name = "GuildID"
    type = "N"
  }

  lifecycle {
    create_before_destroy = true
  }

  tags = {
    Name    = var.dynamodb_table_name
    Project = var.project
  }
}
