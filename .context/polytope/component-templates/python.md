# Directives for Creating A Python Component

## Creating the component
Create a separate directory for the component, even if it's the only component you are creating.

Use the create-component Polytope module to create the project via 
`pt run --non-interactive "create-component{template: python-api, path: my-component-root-path}"`. 

## Specific packages to use
For api servers, use fastapi with uvicorn.
