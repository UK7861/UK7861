from crewai.tools import BaseTool
import pandas as pd
import json

class DataCleaningTool(BaseTool):
    name: str = "data_cleaning_tool"
    description: str = "Cleans data by removing nulls and duplicates. Input should be a JSON string of data."

    def _run(self, data_str: str) -> str:
        try:
            data = json.loads(data_str)
            df = pd.DataFrame(data)
            df = df.drop_duplicates().dropna()
            return df.to_json(orient='records')
        except Exception as e:
            return f"Error cleaning data: {str(e)}"

class BIAutomationTool(BaseTool):
    name: str = "bi_automation_tool"
    description: str = "Mimics outputs for Tableau/PowerBI. Input should be a JSON string of data."

    def _run(self, data_str: str) -> str:
        try:
            data = json.loads(data_str)
            # Mocking BI logic: summarizing metrics
            summary = {
                "total_records": len(data),
                "status": "BI Ready",
                "insights": "Generated mock insights for BI dashboard."
            }
            return json.dumps(summary)
        except Exception as e:
            return f"Error in BI automation: {str(e)}"

class DataDistributor(BaseTool):
    name: str = "data_distributor"
    description: str = "Partitions engines to shard workloads. Input is a task description."

    def _run(self, task_description: str) -> str:
        return f"Task '{task_description}' distributed across 10 specialized agents."

class ReportSynthesizer(BaseTool):
    name: str = "report_synthesizer"
    description: str = "Consolidates final reporting structures. Input is a string of combined agent outputs."

    def _run(self, agent_outputs: str) -> str:
        return f"# Final Mission Report\n\n{agent_outputs}\n\n**Status: Completed**"

# Exporting instances for CrewAI
data_cleaning_tool = DataCleaningTool()
bi_automation_tool = BIAutomationTool()
data_distributor = DataDistributor()
report_synthesizer = ReportSynthesizer()
