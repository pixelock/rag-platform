# coding: utf-8

from collections import Counter
from typing import Optional, Any, List, Mapping
from langchain.llms.base import LLM
from langchain.callbacks.manager import CallbackManagerForLLMRun

from protocols.llms import LLM as LLMType
from protocols.llms import LLMMaxToken
from protocols.api import ChatMessage, ChatCompletionRequest, ChatCompletionResponse
from utils.log import logger
from utils.request import safe_retry_request


class RemoteLLM(LLM):
    url: str
    authorization: str
    model_name: str
    n: int = 1
    max_tokens: Optional[int] = None
    temperature: float = 0.5
    top_p: float = 0.7
    with_stream: bool = False
    system_prompt: Optional[str] = '请你用中文回答下面的问题。'
    retry: int = 3
    retry_delta: int = 3
    timeout: int = 60
    verbose: bool = False

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        max_tokens = self.max_tokens or LLMMaxToken[LLMType(self.model_name)]
        max_completion_tokens = max_tokens - len(prompt)

        messages = []
        if self.system_prompt is not None:
            messages.append(ChatMessage(role='system', content=self.system_prompt))
            max_completion_tokens -= len(self.system_prompt)

        messages.append(ChatMessage(role='user', content=prompt))
        max_completion_tokens -= len(prompt)

        request = ChatCompletionRequest(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            top_p=self.top_p,
            n=self.n,
            max_tokens=max_completion_tokens,
            stream=self.stream
        )
        payload = request.model_dump(mode='json')

        texts = self.get_answer_texts(payload=payload)

        if len(texts) == 1:
            return texts[0]

        c = Counter(texts)
        res = c.most_common(1)[0][0]
        return res

    def get_answer_texts(self, payload):
        texts = None
        resp_json = safe_retry_request(
            url=self.url,
            json_=payload,
            headers={'Authorization': self.authorization},
            timeout=self.timeout,
            retry=self.retry,
            retry_delta=self.retry_delta,
            verbose=self.verbose,
        )

        if resp_json is not None:
            try:
                resp = ChatCompletionResponse(**resp_json)
                texts = [choice.message.content for choice in resp.choices]
            except KeyError as e:
                logger.warning(f'llm request params: {payload}')
                logger.warning(f'llm gateway error reason: {resp_json}')

        return texts

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        return {
            'model_name': self.model_name,
        }

    @property
    def _llm_type(self) -> str:
        return self.model_name
