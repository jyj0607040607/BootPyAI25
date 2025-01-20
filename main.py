from fastapi import FastAPI     # 파이썬 웹 개발 api
from pydantic import BaseModel  # 유효성 검사용 판다틱
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
# 요청(requrest)과 응답(responce)  사이에 특정 작업 수행
# 미들웨어는 모든 요청에 대해 실행되며, 요청을 처리하기 전에 응답을 반환하기 전에 특정 작업을 수행할수 있음
# 예를 들어 로김, 인증, cors처리, 입출등등...
import logging  # 로그 출력용

from starlette.requests import Request
from starlette.responses import Response

app = FastAPI(      # 생성자를 통해서 postman 을 대체하는 문서화를 내장되어 있음
    title="MBC AI 프로젝트 test",
    description="파이썬과 자바부트를 연동한 ai 앱",
    version="1.0.0",
    docs_url=None,  #http://localhost:8001/docs     # 보완상 None 처리한다.
    #redoc_url=None
)                 # fastAPI() 객체 생성해서 app 변수에 넣음

class Item(BaseModel):          # 아이템 객체 생성 (BaseModel : 객체 연결 --> 상속)
    name : str                  # 상품명 : 문자열
    description : str = None    # 상품설명 : 문자열(null)
    price : float               # 가격 : 실수형
    tax : float = None          # 세금 : ( null)

    # 컨트롤러 검증은 postman으로 활용해 보았는데 내장된 백점증 틀도 있다.
class LoggingMiddleware(BaseHTTPMiddleware):        # 로그를 콘솔에 출력하는 용도 1 usage
    logging.basicConfig(level=logging.INFO)         # 로그 출력 추가
    async def dispatch(self, request: Request, call_next) :
        logging.info(f"Req: {request.method}{request.url}")
        resource = await call_next(request)
        logging.info(f"Status Code : {resource.status_code}")
        return resource
app.add_middleware(LoggingMiddleware)       # 모든 요청에 대해 로그를 남기는 미들웨어 클래스를 사용함
@app.get("/")       #http://ip주소:포트/ (루트컨텍스트)
async def read_root():
    return { "HELLO" : "world" }

@app.post("/items/")            # post 메서드용 응답
async def create_item(item: Item):      # BaseModel은 데이터 모델링을 쉽게 도와주고 유효성검사도 수행
    # 잘못된 데이터가 들어오면 422 오류코드를 반환
    return item

@app.get("/items/{item_id}")          # http://ip주소:포트/items/1
async def read_item(item_id: int, q: str =None):
    return {"item_id" : item_id, "q" : q}
    # item_id : 상품의 번호 -> 경로 매개변수
    # q : 쿼리 매개변수 (기본값 none)