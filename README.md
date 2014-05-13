#Mode Reference Data

This repository contains code used to generate many of the reference tables in Mode. All of these tables can be found in the [Reference](https://modeanalytics.com/reference) organization on [Mode](https://modeanalytics.com/). Data is publically available directly via Mode, and can be found at `[reference_type].[table_name]`.

For example, a lookup table containing a list of holidays by country was uploaded to the `reference_lookups` namespace, into a table called `holidays_by_country`. This table can be queried in Mode with the following query:
  
    SELECT *
      FROM reference_lookups.holidays_by_country    


Reference Type | Table Name | Description | Folder
---|---------|-------------|------------
reference_lookups | holidays_by_country | A list of every holiday by country, between May 2014 and May 2015. Source: http://www.qppstudio.net/ | `holidays`
reference_lookups | bls_occupation_codes | A list of every occupation provided by the BLS, including major and minor category codes. Source: http://www.bls.gov/oes/current/oes_stru.htm | `bls-job-titles`
reference_lookups | bls_occupation_examples | Examples of jobs within each BLS occupation. Source: http://www.bls.gov/soc/soc_2010_direct_match_title_file.xls | `bls-job-titles`

