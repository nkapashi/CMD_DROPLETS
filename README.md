

# CMD_DROPLETS

A command line utility to create, start, stop, and delete droplet instances in DigitalOcean cloud. 

## Getting Started

Edit "droplets.json" to match your droplet preferences. Documentation is available here:

https://developers.digitalocean.com/documentation/v2/

###Examples

- Create  droplet instance

  ```
  Select an option: 1 - List, 2 - Delete, 3 - Create > 3
  provide a name > test
  
  test [99495726, '46.101.139.7']
  ```

- List all droplet instances

  ```
  Select an option: 1 - List, 2 - Delete, 3 - Create > 1
  
  test [99495726, '46.101.139.7']
  ```

- Delete Droplet

  ```
  Select an option: 1 - List, 2 - Delete, 3 - Create > 2
  provide droplet name to delete > test
  
  No active droplets found.
  ```
###Requirements
**Python 3**  