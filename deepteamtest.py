import asyncio, requests, os
from deepteam import red_team
from deepteam.vulnerabilities import Misinformation, Robustness, PromptLeakage
from deepteam.attacks.multi_turn import LinearJailbreaking
from dotenv import load_dotenv

load_dotenv()
ID = os.environ["RAG_SEQHUB_API"]

class ApiRequest():
    prompt: str
    chat_history: str

async def model_callback(user_input: str) -> str:
    loop = asyncio.get_running_loop()
    apirequest = ApiRequest.__new__(user_input, "")
    response = loop.run_in_executor(None, requests.get, f"https://ben.seqhubai.com/?id={ID}", apirequest)
    return await response.response

misinfo = Misinformation(types=["factual errors", "unsupported claims"])
robust  = Robustness(types=["hijacking", "input overreliance"])
prompt_leak = PromptLeakage(types=["instructions", "permissions and roles"])
jailbreaking = LinearJailbreaking()

risk_assessment = red_team(
    model_callback=model_callback,
    vulnerabilities=[misinfo, robust, prompt_leak],
    attacks=[jailbreaking],
    attacks_per_vulnerability_type=4,
    target_purpose=(
        "be safe, avoid PII/sensitive leakage, and refuse out-of-scope or unsafe requests."
    ),
)