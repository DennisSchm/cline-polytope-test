# Directives for Creating A Python Component

## Creating the component
**CRITICAL**: ALWAYS make sure that the template argument points inside the `.templates/` directory!

Use the create-component Polytope module to create the project via 
`pt run --non-interactive "create-component{template: python-api, path: my-component-root-path}"`. 

## Specific packages to use
For api servers, use fastapi with uvicorn.
