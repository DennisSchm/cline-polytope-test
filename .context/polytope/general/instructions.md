<instructions>
<title>Instructions to follow when generating code that should run on Polytope</title>

<critical_rules>
<rule_pt_param>NEVER use pt.value - ALWAYS use pt.param instead!</rule_pt_param>
**CRITICAL**: `pt.value` requires users to manually set values in a separate step, which is error-prone and inconvenient.

<example_wrong>
<code language="yaml">
env: [{ name: RPK_BROKERS, value: "{pt.value redpanda-host}:{pt.value redpanda-port}" }]
</code>
</example_wrong>

<example_correct>
<code language="yaml">
params:
  - id: redpanda-host
    type: [default, str, redpanda]
  - id: redpanda-port
    type: [default, int, 9092]
# ...
env: [{ name: RPK_BROKERS, value: "{pt.param redpanda-host}:{pt.param redpanda-port}" }]
</code>
</example_correct>

Values are global state shared between all runs. ALWAYS declare module params and use `pt.param` instead!
For secrets, DO use `pt.secret` - but then you'll have to tell the user to set the secret via `pt secret set <secret-name> <value>` before running Polytope.

<rule_no_after>In templates, don't provide `after` unless steps must wait for another step to complete</rule_no_after>
**CRITICAL**: In a Polytope template that defines a stack of services, NEVER use `run-when: after` for services!

Services that use `polytope/container` BLOCK until the container shuts down. Using `after` would mean waiting forever!

<example_wrong>
<code language="yaml">
run:
  - redpanda
  - module: api
    run-when:
      after: redpanda  # This will wait forever!
</code>
</example_wrong>

<example_correct>
<code language="yaml">
run:
  - redpanda
  - api  # Runs concurrently!
  - frontend  # All services start together
</code>
</example_correct>

All services must be fault-tolerant and handle connection failures gracefully with retries.

<rule_persistent_volumes>ALWAYS use persistent volumes for stateful services</rule_persistent_volumes>
**CRITICAL**: Services like databases, message queues, and caches MUST have persistent volumes or data will be lost on restart.

<example_wrong>
<code language="yaml">
templates:
  - id: stack
    run:
      - polytope/redpanda  # NO! Data will be lost!
</code>
</example_wrong>

<example_correct>
<code language="yaml">
modules:
  - id: redpanda
    module: polytope/redpanda
    args:
      data-volume:
        type: volume
        scope: project # ALWAYS use project scope for persistent data! The default scope is job, which is ephemeral.
        id: redpanda-data

templates:
  - id: stack
    run:
      - redpanda  # Uses your wrapper with volume
</code>
</example_correct>
</critical_rules>

<best_practices>
<concise_templates>Concise template section</concise_templates>
Make the template section of the `polytope.yml` file as short as possible. Define modules under the modules section or use pre-existing Polytope modules and refer to them from the template run section.

Keep names simple, and don't set other ids in templates unless you have multiple calls to the same module.

Don't needlessly add template params. The default params on the module should be sufficient for most use cases.

<sensible_parameters>Give modules sensible parameters</sensible_parameters>
Try to provide default values for all parameters in the modules you write. Prefer parameters to 'hard-coding' values in the module, especially if they're repeated or can be expected to change.

<no_hardcoded_values>No hard coded property values that the user may want to change between deployment environments</no_hardcoded_values>
In the polytope.yml file, all values that may change between deployment environment should be dynamically loaded from Polytope secrets and values, e.g. all ports, hostnames, and protocols should be stored as Polytope values and all usernames, passwords and api keys should be stored as Polytope secrets. All property values specified in a ServiceSpec or EnvVarSpec should be referenced as Polytope values, e.g. port: pt.value api_port. Ensure that no property value inside of a ServiceSpec of EnvVarSpec is hard coded.

<hostnames>Hostnames</hostnames>
The hostnames that web apps need, must be based on Polytope values, so they can be dynamically set to different values in deployment different environments.

The Polytope service hostnames that are accessible internally within a template are not available to a web browser or any other software running outside of Polytope.

<fault_tolerance>Any services you write must be fault tolerant</fault_tolerance>
Don't assume that other services are always up and running. If a service is not available, your service should handle the error gracefully and retry later. This applies to all services, including databases, message queues, and other dependencies.

<realtime_patterns>Real-time applications require special patterns</realtime_patterns>
For applications using WebSockets, background threads, and message queues (like Kafka/Redpanda), refer to the **Real-time Application Patterns** guide in `.context/polytope/templates/realtime-patterns.md`. This covers critical event loop integration patterns to avoid common mistakes like using `asyncio.run()` in background threads.

<executables>Executables</executables>
Ensure that all files to be executed are executable.
</best_practices>

<module_guidelines>
<module_inheritance>Module inheritance</module_inheritance>
Try to stick to the built-in modules. If there's no suitable module for what you're trying to achieve, create a custom module that calls `polytope/container`. 

You can also call modules from `polytope.yml` files in subprojects by making use of the `include` keyword in the polytope file in the root like this: 

<code language="yaml">
include: [
  path/to/subproject/polytope/file
]
modules:
...
</code>

<file_layout>Polytope file layout</file_layout>
Prefer creating modules for the different execution units of your application, e.g. redpanda, etc.

Avoid putting module data directly in templates if it makes sense to be able to run the module directly.
</module_guidelines>

<scaffolding>
<using_scaffold>Using polytope/scaffold</using_scaffold>
When using the `polytope/scaffold` module:
- `template`: Points to the path where the template is stored (e.g., `.templates/python-api`, `.templates/frontend`)
- `path`: Points to the directory where the new project will be created

<example>
`pt run --raw "polytope/scaffold{template: '.templates/python-api', path: 'my-api'}"`
</example>

Be aware that the generated component directories will already contain their own polytope.yml file. After generating a component, update the root `polytope.yml` file to include that file (example: if you create a component `my-component`, add ` - my-component/polytope.yml` in the `include` block in `$repo_root/polytope.yml`).

<write_for_polytope>Write stuff to be run in Polytope</write_for_polytope>
Want to create a test script? Put it in a separate directory and create a module for it (is it a shell script? just use `polytope/container` with `image: alpine` or whatever). Ditto for any other runnable units of code!

If you have different commands in your app, create corresponding run scripts in `bin/` and create a specialized module, e.g.:

<example>
<code language="yaml">
modules:
  - id: api
    module: polytope/python
    params:
      - id: cmd
        type: [default, str, "bin/run"]
    args:
      id: my-app
      image: python:3.13-slim
      code: { type: host, path: . }
      cmd: pt.param cmd

  - id: api-test
    module: api
    params: {cmd: "bin/test"}

  - id: api-ipython
    module: api
    params: {cmd: "bin/ipython"}
</code>
</example>
</scaffolding>
</instructions>
