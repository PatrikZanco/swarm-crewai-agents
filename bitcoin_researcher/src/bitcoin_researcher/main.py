import sys
#!/usr/bin/env python
from bitcoin_researcher.crew import BitcoinResearcherCrew
#input_cmd = sys.argv[1]

def run():
    # Replace with your inputs, it will automatically interpolate any tasks and agents information
    inputs = {
        'topic': "ultimas noticias sobre o bitcoin no mes de junho de 2024"
    }
    BitcoinResearcherCrew().crew().kickoff(inputs=inputs)