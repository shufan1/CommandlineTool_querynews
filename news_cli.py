#!/usr/bin/env python
from news import athena_query
import click

## build comand tool with click()
#when, where, who, what
@click.command()
@click.option('--sql', help="SQL Query String")
@click.option('--year', help="year")
@click.option('--yearmonth', help="month") #if month given,ignore
@click.option('--yearmonthday', help= "specific day formated in YYYYMMDD") #if given, ignore year and month
@click.option('--name', help="name for actor1 or actor2, captalized and full name") #could be actor1 or actor2
@click.option('--country', help="Actor1CountryCode")
@click.option('--orderby', help="Order by which value, must specify descending or ascending with --orderoption")
@click.option('--order',help="choose between 'descending' and 'ascending'")
def athena_query_cli(sql,year,yearmonth,yearmonthday,name,country,orderby,order):
    if sql!=None:
        sql_string = sql
    else:
        sql_template = """SELECT events.globaleventid,events.year,events.monthyear,events.day,events.eventcode,
                        events.actor1name,events.actor2name,events.actor1countrycode,events.actor2countrycode, gdelt.eventcodes.description,events.sourceurl
                        FROM gdelt.events 
                        LEFT JOIN gdelt.eventcodes ON events.eventcode = gdelt.eventcodes.code WHERE """
        condition = []
        if yearmonthday != None:
            condition.append(f"day=%d "%int(yearmonthday))
        if yearmonth != None:
            condition.append( f"monthyear=%d "%int(yearmonth))
        if year != None:
            condition.append(f"year=%d "%int(year))
        if name != None:
            condition.append(f"(actor1name='%s' OR actor2name='%s')"%(name,name))
        if country != None:
            condition.append(f"(actor1countrycode='%s' OR actor2countrycode='%s')"%(country,country))
        condition_string = "AND ".join(condition)
        
        order_string = ""
        if orderby!="":
            order_string+=" ORDER BY events.%s "%orderby
            order_string += "ASC" if order=='ascending' else 'DESC'
        sql_string = sql_template+condition_string+order_string+" LIMIT 20"
        print(sql_string)
    try:
        location,result_df = athena_query(sql_string)
        click.echo("Ouput S3 bucket: %s"%location)
        click.echo("Result:\n")
        click.echo(result_df)
    except:
        click.echo("No result matches from the database. Or error encountered. Try limiting your search.")
    
# def make_query_string():
    


if  __name__=="__main__":
    athena_query_cli()
    
    

