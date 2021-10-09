#!/usr/bin/env python
from news import athena_query
import click

## build comand tool with click()
@click.command()
@click.option('--sql', help="SQL Query String")
def athena_query_cli(sql):
    location,result_df = athena_query(sql)
    click.echo("Ouput S3 bucket: %s"%location)
    click.echo("Result:\n")
    click.echo(result_df)
    


if  __name__=="__main__":
    athena_query_cli()
    
    

