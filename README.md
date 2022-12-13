## INFO ##

The component supports [AB BLE Gateway](https://wiki.aprbrother.com/en/AB_BLE_Gateway_V4.html). 

* It will subscribe MQTT data from `AB BLE gateway` and send to the `bluetooth` component of Home assistant.
* BLE gateway works like an external BLE scanner for HA

At least Home Assistant version 2022.10 is required for the integration.

## Adding the integration ##

* Using the tool of choice open the directory (folder) for your HA configuration (where you find configuration.yaml).
* If you do not have a `custom_components` directory (folder) there, you need to create it.
* In the `custom_components` directory (folder) create a new folder called ab_gateway.
* Download all the files from the `custom_components/ab_gateway/` directory (folder) in this repository.
* Place the files you downloaded in the new directory (folder) you created.
* Restart Home Assistant
* In the HA UI go to `Configuration` -> `Integrations` click "+" and search for `Integration AB Gateway`

Using your HA configuration directory (folder) as a starting point you should now also have this:

```
custom_components/ab_gateway/translations/en.json
custom_components/ab_gateway/__init__.py
custom_components/ab_gateway/ble_parser.py
custom_components/ab_gateway/config_flow.py
custom_components/ab_gateway/const.py
custom_components/ab_gateway/discovery.py
custom_components/ab_gateway/manifest.json
custom_components/ab_gateway/strings.json
```

## Configuration ##

* Configuration `Discovery Prefix of the topic` in the UI. The default prefix is `ab_gateway` and component subscribe the topic `ab_gateway/+`

## Troubleshooting ##

If you have problems with the integration you can add debug prints to the log.

```
logger:
  default: info
  logs:
    custom_components.ab_gateway: debug
```

If you are having issues and want to report a problem, always start with making sure that you're on the latest version of the integration, `ab_gateway` and Home Assistant.

