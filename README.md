# RPA Coding Challenge

This repository contains a Robocorp RPA (Robotic Process Automation) project that scrapes news data from the LA Times website. This guide will help you set up and run the project.

## Project Structure
~~~
.
├── chromedriver
├── conda.yaml
├── config.json├
├── requirements.txt
├── robot.yaml
├── src
│ ├── init.py
│ ├── models
│ │ ├── browser.py
│ │ ├── init.py
│ │ ├── la_landing_page.py
│ │ ├── la_search_page.py
│ │ └── pycache
│ └── utils
│ ├── count_words.py
│ ├── has_money.py
│ ├── init.py
│ ├── is_within_range.py
│ ├── month_diff.py
│ 
├── tasks.py
└── tests
├── init.py

├── test_browser.py
├── test_count_words.py
├── test_has_money.py
├── test_is_within_range.py
├── test_la_landing_page.py
├── test_la_search_page.py
└── test_month_diff.py

~~~

## Setup

### Prerequisites

1. **Robocorp CLI (rcc)**: Make sure you have Robocorp CLI installed. You can follow the instructions on the [Robocorp website](https://robocorp.com/docs/developing-robot/rcc) to install it.

2. **Python**: Ensure that Python 3.11.9 or later is installed.

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/rpa-coding-challenge.git
   cd rpa-coding-challenge
   pip install -r requirements.txt


### Configuration

Create config.json

The config.json file should include the necessary configuration parameters for the project. Here is an example of what the file might look like:


    {
      "search_term": "Stocks",
      "filter": "Business",
      "month_range": 2
    }
    Adjust the values according to your needs.

## Running the Project

To run the RPA project using Robocorp CLI:

    Run the Tasks

    bash

    rcc run

    This will execute the tasks defined in robot.yaml and use the configuration from config.json.

    Check the Output

    The results of the RPA tasks will be saved in the output directory. This includes logs, screenshots, and data files.

### Creating a robot 
~~~
rcc robot wrap -d <YOUR-DIR>
~~~
Pushing to RCC Clou
~~~
rcc cloud push -r <ROBOT-ID> -w <WORKSPACE-ID>
~~~
### Testing
~~~
pytest -v
~~~
This will run all tests defined in the tests directory.

### Troubleshooting

    Check Logs: If you encounter issues, check the log files in the output directory for more details.
    Screenshot Errors: Screenshots of browser errors are saved in the output directory with filenames indicating the type of error.