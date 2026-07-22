from fastapi.routing import APIRoute
from fastapi.responses import JSONResponse
from fastapi import Request


class ResponseRoute(APIRoute):

    def get_route_handler(self):
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request):
            response = await original_route_handler(request)

            if isinstance(response, dict):

                return JSONResponse(
                    content={
                        "success": True,
                        "message": response.get(
                            "message",
                            "Success"
                        ),
                        "data": response.get(
                            "data"
                        ),
                        "meta": response.get(
                            "meta"
                        ),
                        "errors": None
                    }
                )

            return response

        return custom_route_handler