# Moottori - bensatankki sekvenssikaaviona

```mermaid
  sequenceDiagram
    call->>Machine.__init__:init Machine
    Machine.__init__->>self._tank:prep new FuelTank for machine
    self._tank->>FuelTank.__init__:init FuelTank
    FuelTank.__init__-->>self._tank:save new FuelTank
    Machine.__init__->>self._tank.fill:fill the tank
    Machine.__init__->>self._engine:prep new Engine for machine
    self._engine->>Engine.__init__:init engine with fueltank
    Engine.__init__-->>self._engine:save new Engine
    Engine
    FuelTank
```