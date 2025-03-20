# CEX-API-Latency-Monitor





# Structure

```
api-latency-monitor/          
│── .github/                  # GitHub Actions config files
│   ├── workflows/
│   │   ├── api_latency_measurement.yml   
│   │   ├── api_latency_report.yml        
│── latency_monitor/            
│   ├── __init__.py             
│   ├── test_api_latency.py    # the pytest test file
│   ├── latency_logger.py      
│   ├── generate_report.py      
│── reports/                    
│   ├── latency_trend.png      # the latency trend graph
│── data/                       
│   ├── latency_log.json       # store the latency data
│── pyproject.toml            
│── README.md                 

```
