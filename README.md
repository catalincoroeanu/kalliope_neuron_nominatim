# Nominatim

## Synopsis
Neuron to use the OpenStreetMap's [Nominatim](https://nominatim.openstreetmap.org/) API to

* get coordinates from an address
* get an address from coordinates

## Installation
```
kalliope install --git-url https://github.com/redSpoutnik/kalliope_neuron_nominatim.git
```

## Options

| parameter  | required                     | default | choices                | comment |
|------------|------------------------------|---------|------------------------|---------|
| operation  | YES                          | None    | "geocode" or "reverse" |         |
| language   | NO                           | False   | string                 | Preferred language in which to return results. Uses standard [RFC2616](http://www.ietf.org/rfc/rfc2616.txt). |
| address    | YES if operation = "geocode" | None    | string                 |         |
| latitude   | YES if operation = "reverse" | None    | string                 | The string should only represent an integer or float number. |
| longitude  | YES if operation = "reverse" | None    | string                 | The string should only represent an integer or float number. |

* **"geocode"** operation performs **geocoding** (address -> coordinates) using **address** parameter
* **"reverse"** operation performs **reverse geocoding** (coordinates -> address) using **latitude** and **longitude** parameters

## Return Values

| Name       | Description                      | Type   |
|------------|----------------------------------|--------|
| raw        | Raw json from API response       | string |
| address    | Address of requested location    | string |
| latitude   | Latitude of requested location   | float  |
| longitude  | Longitude of requested location  | float  |

* **address** returned from **"geocode"** operation is the full address for location found, it overwrites the input address.
* **latitude** and **longitude** returned from **"reverse"** operation are the exact coordinates for location found, it overwrites the input coordinates.

## Synapses example

Get coordinates from an input address

```yaml
  - name: "nominatim-geocode"
    signals:
      - order: "get coordinates of {{ address }}"
    neurons:
      - nominatim:
          language: "en"
          operation: "geocode"
          address: "{{ address }}"
          say_template: "lattitude {{ latitude }} and longitude {{ longitude }}"
```

Get an address from input coordinates

```yaml
  - name: "nominatim-reverse"
    signals:
      - order: "get address for coordinates latitude {{ latitude }} and longitude {{ longitude }}"
    neurons:
      - nominatim:
          language: "en"
          operation: "reverse"
          latitude: "{{ latitude }}"
          longitude: "{{ longitude }}"
          say_template: "{{ address }}"
```

Get complete location

```yaml
  - name: "nominatim-full-geocode"
    signals:
      - order: "get location for address {{ address }}"
    neurons:
      - nominatim:
          language: "en"
          operation: "geocode"
          address: "{{ address }}"
          say_template: "found location {{ address }} with latitude {{ latitude }} and longitude {{ longitude }}"

  - name: "nominatim-full-reverse"
    signals:
      - order: "get location for latitude {{ latitude }} and longitude {{ longitude }}"
    neurons:
      - nominatim:
          language: "en"
          operation: "reverse"
          latitude: "{{ latitude }}"
          longitude: "{{ longitude }}"
          say_template: "found location {{ address }} with latitude {{ latitude }} and longitude {{ longitude }}"
```