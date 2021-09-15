# DQN_asset_allocation
Stock/Bond allocation with DQN
## Environment
1. State: (agent's current equity weight, equity return on recent 120days, equity volatility on recent 120days, equity return on recent 20days, equity volatility on recent 20days)
2. Action: increase stock weight by 5%p, decrease by 5%p, do nothing
3. Reward: Log-return

## Agent
Dual-Deep Q-network & Epsilon-greedy policy

<img src="https://user-images.githubusercontent.com/73049948/133425142-6e2c212d-bfca-46e2-8530-bd8d7c7b17a3.PNG" width="500">

## Reward curve
![score](https://user-images.githubusercontent.com/73049948/133425385-b0d5f260-c3d3-4174-9019-ab8f379f8ec0.PNG)

## Action behavior
![action](https://user-images.githubusercontent.com/73049948/133425424-9b5c151b-74a8-46cd-834c-846f4a3cc588.PNG)

## In-sample test result
![asset](https://user-images.githubusercontent.com/73049948/133425457-07181292-b6c0-4d5d-a7b6-8a6856783e16.PNG)
