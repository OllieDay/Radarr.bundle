# Radarr.bundle
Plex agent that retrieves metadata from Radarr.

## Installation
- Download the latest release from [https://github.com/OllieDay/Radarr.bundle/releases/latest](https://github.com/OllieDay/Radarr.bundle/releases/latest)
- Extract the archive and rename it to `Radarr.bundle`
- Move `Radarr.bundle` to the Plex directory `config/Library/Application Support/Plex Media Server/Plug-ins`
- Restart Plex to load the agent

## Usage
There are 2 options you have:

1. You can use the agent as a standalone (primary) agent. That way only data from Radarr will be used. Please note that this will not give you the same data rich library you're probably used to. Most important data will be present, but some pieces will be missing, because Radarr doesn't provide some details.
2. You can use the agent as a secondary agent to Plex Movie agent. Activate it under Plex Movie in *Settings* > *Server* > *Agents* > *Movies*. Drag it to just below Plex Movie to let this agent fill in the blanks from Plex Movie.

Before using the agent, go into the agent's preferences and enter your Radarr URL and API key (you can find your Radarr API key in Radarr under *Settings* > *General* > *Security*).

Based on [piplongrun/Sonarr.bundle](https://github.com/piplongrun/Sonarr.bundle) Plex Sonarr agent.
