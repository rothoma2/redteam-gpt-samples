from langchain_community.llms import OpenAI
from langchain_community.tools import DuckDuckGoSearchRun
from crewai import Agent, Task, Crew, Process
import os
from crewai_tools import BaseTool
import subprocess
from typing import List, Optional

class RunRawLinuxCommandTool(BaseTool):
    name: str = "Run Raw Linux Command"
    description: str = "Executes a raw Linux command as a last resort when no more specific tool is available."

    def _run(self, command: str) -> str:
        try:
            # Execute the raw Linux command
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True
            )
            
            # Check if the command was successful
            if result.returncode == 0:
                return result.stdout
            else:
                return f"Error: Command failed with error: {result.stderr}"
        except Exception as e:
            return f"Exception occurred: {str(e)}"

class NmapHostDiscoveryTool(BaseTool):
    name: str = "Nmap Host Discovery"
    description: str = "Scans the network to identify hosts that are online using Nmap."

    def _run(self, target_network: str) -> str:
        try:
            # Run the Nmap command for host discovery (-sn disables port scanning)
            result = subprocess.run(
                ["nmap", "-sn", target_network],
                capture_output=True,
                text=True
            )
            # Check if the command was successful
            if result.returncode == 0:
                return result.stdout
            else:
                return f"Error: Nmap scan failed with error: {result.stderr}"
        except Exception as e:
            return f"Exception occurred: {str(e)}"

class NmapPortAndServiceScanTool(BaseTool):
    name: str = "Nmap Port and Service Scan"
    description: str = "Performs a scan to identify open ports and determines the services running on those ports using Nmap."

    def _run(self, target: str) -> str:
        try:
            # Run the Nmap command to identify open ports and perform service identification (-sV for service/version detection)
            result = subprocess.run(
                ["nmap", "-sV", target],
                capture_output=True,
                text=True
            )
            
            # Check if the command was successful
            if result.returncode == 0:
                return result.stdout
            else:
                return f"Error: Nmap scan failed with error: {result.stderr}"
        except Exception as e:
            return f"Exception occurred: {str(e)}"

class HumanVerificationTool(BaseTool):
    name: str = "Human Verification"
    description: str = "Asks a verification question to the human pentester and takes keyboard input when in doubt."

    def _run(self, question: str) -> str:
        # Ask the verification question
        print(f"Verification needed: {question}")
        
        # Prompt the pentester for input
        user_input = input("Please enter your response: ")
        
        # Return the pentester's response
        return user_input

class DirbDirectoryDiscoveryTool(BaseTool):
    name: str = "Dirb Directory Discovery"
    description: str = "Discovers directories and files on the target web server using the `dirb` tool."

    def _run(self, target_url: str) -> str:
        """
        Runs the dirb tool against the specified target URL with the given wordlist.

        :param target_url: URL of the web server to scan
        :param wordlist: Path to the wordlist file to use for discovery
        :return: Output from the dirb scan
        """
        try:
            result = subprocess.run(
                ["dirb", target_url],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return result.stdout
            else:
                return f"Error: Dirb scan failed with error: {result.stderr}"
        except Exception as e:
            return f"Exception occurred: {str(e)}"


class GobusterDirectoryDiscoveryTool(BaseTool):
    name: str = "Gobuster Directory Discovery"
    description: str = "Uses `gobuster` to enumerate directories and files on a web server."

    def _run(self, target_url: Optional[str] = None, wordlist: str = "/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt") -> str:
        """
        Runs the gobuster tool against the specified target URL with the given wordlist.

        :param target_url: URL of the web server to scan
        :param wordlist: Path to the wordlist file to use for discovery
        :return: Output from the gobuster scan
        """
        # Validate the target URL and wordlist
        if not target_url:
            return "Error: The target URL must be specified."
        if not wordlist:
            return "Error: The wordlist path must be specified."

        # Construct the command as a string for shell=True
        command = f"gobuster dir -u {target_url} -w {wordlist}"
        
        # Print the command for debugging purposes
        print(f"Running command: {command}")

        # Run the command using shell=True
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return result.stdout
            else:
                return f"Error: Gobuster scan failed with error: {result.stderr}"
        except Exception as e:
            return f"Exception occurred: {str(e)}"
        

search_tool = DuckDuckGoSearchRun()
online_hosts_tool = NmapHostDiscoveryTool()
port_scanning_tool = NmapPortAndServiceScanTool()
human_verification_tool = HumanVerificationTool()
linux_command_tool = RunRawLinuxCommandTool()
dirb_discovery_tool = DirbDirectoryDiscoveryTool()
gobuster_discovery_tool = GobusterDirectoryDiscoveryTool()


# Update pentester agent with the new directory discovery tools
pentester = Agent(
    role='Lead Penetration Tester',
    goal='Identify vulnerabilities in the target systems by conducting simulated attacks',
    backstory="""You are a seasoned cybersecurity expert with extensive experience in penetration testing.
    Your deep knowledge of system vulnerabilities and attack vectors allows you to expose weaknesses in any infrastructure.
    The target under assestment is 192.168.2.155 on port 3000""",
    verbose=True,
    allow_delegation=True,
    tools=[search_tool, human_verification_tool,
            linux_command_tool, 
           dirb_discovery_tool, gobuster_discovery_tool]
)

security_analyst = Agent(
  role='Security Operations Analyst',
  goal='Analyze and interpret findings from penetration tests to assess risks and recommend security improvements',
  backstory="""You have a deep understanding of security operations and incident response.
  Your ability to analyze complex security data and translate it into actionable intelligence makes you an invaluable asset.""",
  verbose=True,
  allow_delegation=True,
  tools=[search_tool, linux_command_tool]
  #tools=[search_tool, analysis_tool, reporting_tool]
)

project_manager = Agent(
  role='Penetration Testing Project Manager',
  goal='Coordinate and monitor the progress of the penetration testing project, ensuring timely completion and communication between team members',
  backstory="""You are a skilled project manager with a strong focus on cybersecurity projects.
  Your organizational skills and ability to manage timelines and resources are key to the success of the penetration testing efforts.""",
  verbose=True,
  allow_delegation=True,
  tools=[search_tool]
)

task1_1 = Task(
  description="""Define the specific objectives for the penetration test.
  Determine the key goals, such as identifying exploitable vulnerabilities or testing incident response.""",
  expected_output="Document outlining the objectives of the penetration test",
  agent=project_manager
)

task1_2 = Task(
  description="""List and confirm the systems, networks, and applications that will be in scope for the penetration test.
  Ensure all in-scope items are documented and approved by stakeholders.""",
  expected_output="List of in-scope systems, networks, and applications",
  agent=project_manager
)

task3_1 = Task(
  description="""Perform network scanning to identify active IP addresses and open ports on the target network.
  Use tools like `Nmap` to map the network topology.""",
  expected_output="Network map with active IPs and open ports",
  agent=pentester
)

task3_2 = Task(
  description="""Enumerate services running on open ports identified during network scanning.
  Identify service versions and configurations to detect potential vulnerabilities.""",
  expected_output="List of services with versions and configurations",
  agent=pentester
)

task3_3 = Task(
  description="""Identify the technologies and frameworks used by the web applications in scope.
  Use tools like `WhatWeb` and `Wappalyzer` to gather this information.""",
  expected_output="List of web application technologies and frameworks",
  agent=pentester
)

task_web_directory_discovery = Task(
    description="""Perform directory discovery on the web server to identify hidden directories and files.
    Use tools like `dirb` and `gobuster` to conduct comprehensive scans.""",
    expected_output="List of discovered directories and files on the target web server",
    agent=pentester
)


# task4_1 = Task(
#   description="""Run automated vulnerability scans on the target systems using tools like `Nessus`, `OpenVAS`, or `Qualys`.
#   Identify known vulnerabilities based on CVEs and severity levels.""",
#   expected_output="Automated Vulnerability Scan Report",
#   agent=pentester
# )

task5_1 = Task(
  description="""Attempt to exploit the validated vulnerabilities to gain unauthorized access to the target systems.
  Document the steps, tools used, and access achieved during the exploitation.""",
  expected_output="Exploitation Report with details of successful attacks",
  agent=pentester
)

task5_2 = Task(
  description="""Attempt to escalate privileges on compromised systems to gain higher levels of access.
  Use known techniques and tools like `Metasploit` or `PowerShell`.""",
  expected_output="Privilege Escalation Report with techniques and outcomes",
  agent=pentester
)

task6_1 = Task(
  description="""Compile initial findings from the penetration test, including identified vulnerabilities, exploitation attempts, and their outcomes.
  Prepare a summary for internal review.""",
  expected_output="Initial Findings Summary Document",
  agent=security_analyst
)

task6_4 = Task(
  description="""Compile the final Penetration Testing Report, including all findings, exploitation details, impact assessments, and remediation recommendations.
  Ensure the report is clear and accessible for both technical and non-technical stakeholders.""",
  expected_output="Final Penetration Testing Report",
  agent=security_analyst
)

# Instantiate your crew with a sequential process
crew = Crew(
  agents=[pentester, project_manager],
  tasks=[task3_1, task_web_directory_discovery],
  verbose=2, # You can set it to 1 or 2 to different logging levels
)

# Get your crew to work!
result = crew.kickoff()

print("###########")
print(result)