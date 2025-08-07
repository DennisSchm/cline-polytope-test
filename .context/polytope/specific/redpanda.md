# Documentation on how to use Redpanda in Polytope

## Dev Mode and Topic Creation
When configuring and running redpanda as described in this documentation, it runs in dev mode and creates topics lazily. **No setup to generate topics is needed** - topics are automatically created when first accessed.

## Creating Redpanda Components
Use the redpanda template to automatically generate pre-configured redpanda components. This eliminates the need to manually configure redpanda modules in the root polytope file.

### Generate a Redpanda Component
Use the polytope scaffold command with the redpanda template:

```bash
pt run --raw "polytope/scaffold{template: '.templates/redpanda', path: 'redpanda'}"
```

Examples:
- Server component: `pt run --raw "polytope/scaffold{template: '.templates/redpanda', path: 'redpanda'}"`
- Another server: `pt run --raw "polytope/scaffold{template: '.templates/redpanda', path: 'server'}"`

The generated component includes:
- Pre-configured `polytope.yml` file with redpanda and redpanda console modules
- Proper persistent volume configuration
- All necessary wrapper modules

**IMPORTANT:** The generated `polytope.yml` file is pre-configured and should not be modified unless you need to change the Redpanda cluster configuration.

## Running Redpanda Console
Run the `polytope/redpanda!console` module together with the redpanda server.

This defaults to connecting to the redpanda server running via `polytope/redpanda`, so there's no need to specify any args. Don't try to create a module wrapping this, you'll just trip yourself up.

## For any Python code that accesses redpanda
Use the kafka-python package. Version: 2.2.15

You must check that no python code uses any other version of the kafka-python package.
