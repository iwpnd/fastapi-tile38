<br />
<p align="center">
  <h3 align="center">FastAPI-Tile38</h3>

  <p align="center">
    Showcase using Tile38 via pyle38 in a FastAPI application.
    <br />
    <a href="https://github.com/iwpnd/fastapi-tile38/issues">Report Bug</a>
    ·
    <a href="https://github.com/iwpnd/fastapi-tile38/issues">Request Feature</a>
  </p>
</p>

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project

Showcase of using [Tile38](https://github.com/tidwall/tile38) with [Pyle38](https://github.com/iwpnd/pyle38) in a [FastAPI](https://github.com/tiangolo/fastapi)
application. Can be used as is, or be extended upon with other methods in the [pyle38 repertoire](https://github.com/iwpnd/pyle38#commands) of commands.

### Built With

-   [FastAPI](https://github.com/tiangolo/fastapi)
-   [Pyle38](https://github.com/iwpnd/pyle38)
-   [Tile38](https://github.com/tidwall/tile38)
-   [pydantic](https://github.com/samuelcolvin/pydantic/)

<!-- GETTING STARTED -->

## Getting Started

### Installation

1. Clone and install
    ```sh
    git clone https://github.com/iwpnd/fastapi-tile38.git
    poetry install
    ```
2. Setup environment
    ```sh
    cp .env.dist .env
    ```
3. Start your local stack
    ```python
    docker-compose up
    ```
4. Test it!
    ```sh
    pytest . -vv -s
    ```

## Usage

Once the application is started you can checkout and interact with it via on [localhost:8001/docs](http://localhost:8001/docs).

Or you can use it with [http](https://httpie.io/)/[curl](https://curl.se/):

```sh
echo '{ "data": { "type": "Feature", "geometry": {"type": "Point", "coordinates": [13.37, 52.25]}, "properties": {"id": "truck"}}}' \
      | http post http://localhost:8001/vehicle x-api-key:test

> {
    "elapsed": "37.5µs",
    "ok": true
}


http get http://localhost:8001/search/within lat==52.25 lon==13.37 radius==1000 \
  x-api-key:test

> {
    "data": [
        {
            "id": "truck",
            "object": {
                "geometry": {
                    "coordinates": [
                        13.37,
                        52.25
                    ],
                    "type": "Point"
                },
                "properties": {
                    "id": "truck"
                },
                "type": "Feature"
            }
        }
    ]
}
```

Or you use it with [httpx](https://www.python-httpx.org/)/[requests](https://docs.python-requests.org/en/master/):

```python
import httpx

vehicle = {
    "type": "Feature",
    "geometry": {"type": "Point", "coordinates": [13.37, 52.25]},
    "properties": {"id": "truck"},
}

# store a vehicle
r = httpx.post(
      url="http://localhost:8001/vehicle",
      headers={"x-api-key":"test"},
      json={"data": vehicle}
      )

print(r.json())

> {
    "elapsed": "70.8µs",
    "ok": true
}

# get vehicle in a radius around a location
r = httpx.get(
      url="http://localhost:8001/search/within",
      headers={"x-api-key":"test"},
      params={"lat":52.25,"lon":13.37,"radius":1000}
      )

print(r.json())

> {
    "data": [
        {
            "id": "truck",
            "object": {
                "geometry": {
                    "coordinates": [
                        13.37,
                        52.25
                    ],
                    "type": "Point"
                },
                "properties": {
                    "id": "truck"
                },
                "type": "Feature"
            }
        }
    ]
}
```

You get the idea. And can use the rest.

Inputs are being validated at runtime with [pydantic](https://pydantic-docs.helpmanual.io/).

## License

Distributed under the MIT License. See `LICENSE` for more information.

<!-- CONTACT -->

## Contact

Benjamin Ramser - [@imwithpanda](https://twitter.com/imwithpanda) - ahoi@iwpnd.pw  
Project Link: [https://github.com/iwpnd/fastapi-tile38](https://github.com/iwpnd/fastapi-tile38)
