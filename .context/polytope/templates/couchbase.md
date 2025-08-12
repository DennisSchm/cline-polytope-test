<instructions>
<title>Documentation on how to use Couchbase in Polytope</title>

<dev_mode_setup>
<section_title>Dev Mode and Bucket Creation</section_title>
When configuring and running Couchbase as described in this documentation, it runs in dev mode with default credentials (`user`/`password`). The template includes an `init-couchbase` utility that automatically initializes the cluster and creates the main bucket. **Minimal setup is needed** - the template handles cluster initialization and bucket creation automatically.
</dev_mode_setup>

<component_creation>
<section_title>Creating Couchbase Components</section_title>
Use the couchbase template to automatically generate pre-configured Couchbase components. This eliminates the need to manually configure Couchbase modules in the root polytope file.

<generate_component>
<subsection_title>Generate a Couchbase Component</subsection_title>
Execute the following command in the terminal to use the polytope scaffold command with the couchbase template:
`pt run --raw "polytope/scaffold{template: '.templates/couchbase', path: 'couchbase'}"`

<examples>
<example_title>Examples</example_title>

Database component 
`pt run --raw "polytope/scaffold{template: '.templates/couchbase', path: 'couchbase'}"`

Another database server
`pt run --raw "polytope/scaffold{template: '.templates/couchbase', path: 'database'}"`
</examples>

<generated_features>
The generated component includes:
- Pre-configured `polytope.yml` file with `couchbase-stack` template
- Couchbase server module with persistent volume configuration
- `init-couchbase` utility that automatically:
  - Initializes the cluster with default credentials
  - Creates the main bucket
  - Sets up configuration
- Configurable parameters:
  - `COUCHBASE_USERNAME` (default: `user`)
  - `COUCHBASE_PASSWORD` (default: `password`)

**IMPORTANT:** The generated `polytope.yml` file is pre-configured and should not be modified unless you need to change the Couchbase cluster configuration or credentials.
</generated_features>
</generate_component>
</component_creation>

<api_integration>
<section_title>Integrating APIs with Couchbase</section_title>
To integrate your API modules with Couchbase, configure them to connect using environment variables that match the Couchbase template's default settings.

Add these environment variables to your API module in the couchbase Polytope file:

- `COUCHBASE_URL`: `couchbase://couchbase`
- `COUCHBASE_USERNAME`: `user` (default) 
- `COUCHBASE_PASSWORD`: `password` (default)
- `COUCHBASE_BUCKET`: `main`
- `COUCHBASE_SCOPE`: `_default`

Add the following configuration code.
<code language="python" path="api_name/src/api_name/utils/conf.py">
#### Types ####

class CouchbaseConf(BaseModel):
    url: str
    bucket: str
    username: str
    password: str
    scope: str = "_default"

## Couchbase ##

COUCHBASE_URL      = EnvVarSpec(id="COUCHBASE_URL")
COUCHBASE_BUCKET   = EnvVarSpec(id="COUCHBASE_BUCKET")
COUCHBASE_PASSWORD = EnvVarSpec(id="COUCHBASE_PASSWORD", is_secret=True)
COUCHBASE_SCOPE    = EnvVarSpec(id="COUCHBASE_SCOPE", default="_default")
COUCHBASE_USERNAME = EnvVarSpec(id="COUCHBASE_USERNAME")

#### Validation ####

def validate() -> bool:
    return env.validate(
        [
            LOG_LEVEL,
            HTTP_PORT,
            HTTP_AUTORELOAD,
            COUCHBASE_URL,
            COUCHBASE_BUCKET,
            COUCHBASE_USERNAME,
            COUCHBASE_PASSWORD,
            COUCHBASE_SCOPE,
        ]
    )

def get_couchbase_conf() -> CouchbaseConf:
    return CouchbaseConf(
        url=env.parse(COUCHBASE_URL),
        bucket=env.parse(COUCHBASE_BUCKET),
        username=env.parse(COUCHBASE_USERNAME),
        password=env.parse(COUCHBASE_PASSWORD),
    )
</code>



<client_implementation>
<subsection_title>Implementing a Couchbase Client</subsection_title>

**Example Client Structure:**
create a subdir for the client, then add and customize the following code
<code language="python" path="api_name/src/api_name/clients/resource">
logger = log.get_logger(__name__)

class ResourceNameClient:
    def __init__(
        self,
        url: str = None,
        username: str = None,
        password: str = None,
        bucket_name: str = None,
        scope: str = "_default",
        resource_collection_name_coll: str = "resouces_collection_name",
    ):
        self.url = url
        self.username = username
        self.password = password
        self.bucket_name = bucket_name
        self.scope_name = scope
        self.resource_collection_name_coll = resource_collection_name_coll
        self.cluster = None
        self.bucket = None
        self.scope = None
        self.resource_collection_name = None
        self._is_query_service_ready = False

    def connect(self, max_retries: int = 30, initial_delay: float = 1.0, max_delay: float = 10.0) -> None:
        """
        Establish connection to Couchbase database.

        Args:
            max_retries: Maximum number of retry attempts.
            initial_delay: Initial delay between retries in seconds.
            max_delay: Maximum delay between retries in seconds.
        """
        auth = PasswordAuthenticator(self.username, self.password)
        options = ClusterOptions(auth)

        self.cluster = Cluster(self.url, options)
        delay = initial_delay
        connected = False

        for attempt in range(1, max_retries + 1):
            try:
                self.bucket = self.cluster.bucket(self.bucket_name)
                self.scope = self.bucket.scope(self.scope_name)
                connected = True
                logger.info(f"Connected to Couchbase database with bucket and scope on attempt {attempt}")
                break
            except Exception as bucket_err:
                logger.warning(f"Bucket or scope not ready yet (attempt {attempt}/{max_retries}): {str(bucket_err)}")
                if attempt < max_retries:
                    logger.info(f"Retrying in {delay:.1f} seconds...")
                    time.sleep(delay)
                    # Exponential backoff with a cap
                    delay = min(max_delay, delay * 1.5)
                else:
                    logger.error(f"Failed to connect after {max_retries} attempts")

        if connected:
            try:
                self.init()
            except Exception as col_err:
                logger.warning(f"Collections not ready yet: {str(col_err)}")

    def init(self, max_retries: int = 30, initial_delay: float = 1.0, max_delay: float = 10.0) -> None:
        """
        Create the collections if they don't exist.

        Args:
            max_retries: Maximum number of retry attempts.
            initial_delay: Initial delay between retries in seconds.
            max_delay: Maximum delay between retries in seconds.
        """
        delay = initial_delay

        for attempt in range(1, max_retries + 1):
            try:
                # CRITICAL: Ensure we have a valid cluster connection first
                if not self.cluster:
                    logger.warning("No cluster connection, attempting to connect...")
                    # Don't call self.connect() to avoid recursion, just create cluster
                    auth = PasswordAuthenticator(self.username, self.password)
                    options = ClusterOptions(auth)
                    self.cluster = Cluster(self.url, options)
                
                # Ensure we have bucket and scope
                if not self.bucket:
                    self.bucket = self.cluster.bucket(self.bucket_name)
                if not self.scope:
                    self.scope = self.bucket.scope(self.scope_name)

                collection_manager = self.bucket.collections()

                # Create collections if they don't exist
                for coll in [self.resource_collection_name_coll]:
                    try:
                        collection_manager.create_collection(self.scope_name, coll)
                        logger.info(f"Created collection: {coll}")
                    except Exception as e:
                        if "already exists" in str(e):
                            logger.info(f"Collection {coll} already exists")
                        else:
                            logger.warning(f"Error creating collection {coll}: {str(e)}")

                # Get collection references
                self.resource_collection_name = self.scope.collection(self.resource_collection_name_coll)

                logger.info(f"Collections initialized successfully on attempt {attempt}")
                break

            except Exception as e:
                logger.warning(f"Error initializing collections (attempt {attempt}/{max_retries}): {str(e)}")
                if attempt < max_retries:
                    logger.info(f"Retrying in {delay:.1f} seconds...")
                    time.sleep(delay)
                    # Exponential backoff with a cap
                    delay = min(max_delay, delay * 1.5)
                else:
                    logger.error(f"Failed to initialize collections after {max_retries} attempts")
                    raise

    def await_up(self, max_retries: int = 30, initial_delay: float = 1.0, max_delay: float = 10.0) -> None:
        """
        Wait until the Couchbase query service is available by running a simple query in a loop.

        Args:
            max_retries: Maximum number of retry attempts.
            initial_delay: Initial delay between retries in seconds.
            max_delay: Maximum delay between retries in seconds.
        """
        # If we already know the service is ready, skip the check
        if self._is_query_service_ready:
            return

        if not self.cluster:
            self.connect()

        delay = initial_delay
        for attempt in range(1, max_retries + 1):
            try:
                # Try a simple query that doesn't depend on any collections
                query = "SELECT 1"
                result = self.cluster.query(query)
                # Consume the result to ensure it completes
                list(result)

                # If we got here, the query service is ready
                self._is_query_service_ready = True
                logger.info("Couchbase query service is ready")
                return
            except Exception:
                logger.warning(
                    f"Attempt {attempt}/{max_retries}: Couchbase query service not available yet. "
                    f"Retrying in {delay:.1f} seconds..."
                )
                time.sleep(delay)
                # Exponential backoff with a cap
                delay = min(max_delay, delay * 1.5)

        # If we've exhausted all retries
        raise Exception(f"Couchbase query service not available after {max_retries} attempts")

    # Employee methods
    def create_resource(self, recource_field: str,) -> str:
        """
        Create a new resource.

        Args:
            employee_field: A resource field (like unique identifier or name)
        
        Returns:
            The resource unique identifier
        """
        if not self.resource_collection_name:
            self.init()

        doc = {
            "resource_field_name": recource_field,
        }

        try:
            self.resource_collection_name.upsert(resource_unique_identifier_field, doc)
            logger.info(f"Created resource with number: {resource_unique_identifier_field}")
            return resource_unique_identifier_field
        except Exception:
            logger.exception("Failed to create resource")
            raise

    def get_recource_collection_name(self) -> List[Dict[str, Any]]:
        """
        Get all recource_name.

        Returns:
            List of recource_name
        """
        if not self.resource_collection_name:
            self.init()

        # Make sure the query service is available
        self.await_up()

        try:
            query = f"""
            SELECT e.*
            FROM {self.bucket_name}.{self.scope_name}.{self.resource_collection_name_coll} e
            """

            result = self.cluster.query(query)
            return [row for row in result]
        except Exception:
            logger.exception("Failed to get recource_collection_name.")
            raise

    def close(self) -> None:
        """Close the database connection."""
        if self.cluster:
            self.cluster = None
            logger.info("Database connection closed")

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
</code>

Add the following code to main
<code language="python" path="api_name/src/api_name/main.py">
@asynccontextmanager
async def lifespan(app: FastAPI):
    cb_conf = conf.get_couchbase_conf()
    app.state.db = SchedulingClient(
        url=cb_conf.url,
        username=cb_conf.username,
        password=cb_conf.password,
        bucket_name=cb_conf.bucket,
        scope=cb_conf.scope
    )
    try:
        app.state.db.connect()
        logger.info("Connected to Couchbase database")

    except Exception:
        logger.warning("Couldn't connect to Couchbase - retrying on next request.")
        
    logger.info("Application initialized")

    yield
</code>

add all required models for the resources to `models.py`  

add the following code to routes
<code language="python" path="api_name/src/api_name/routes.py">
def get_db_handle(request: Request) -> ResourceNameClient:
    """Util for getting the Couchbase client from the request state."""
    return request.app.state.db

DbHandle = Annotated[RecourceNameClient, Depends(get_db_handle)]

# Recource Routes
@router.post("/resource-name", response_model=Employee)
async def create_resource_name(
    db: DbHandle,
    request: RecourceNameCreateRequest
) -> Employee:
    """Create a new resource-name."""
    try:
        # CRITICAL: Ensure database connection is ready
        if not db.resource_collection_name:
            try:
                db.init()
            except Exception as init_err:
                logger.error(f"Database not ready: {init_err}")
                raise HTTPException(status_code=503, detail="Database not ready, please try again later")
        
        recource_name_id = db.create_recource_name(
            resource_field_name=request.resource_field_name,
        )
        resource_name = db.get_resource_name(resource_name_id)
        return ResourceName(**resource_name)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to create resource: {e}")
        raise HTTPException(status_code=500, detail="Failed to create resource")

@router.get("/resource-collection-name", response_model=List[ResourceName])
async def get_resource_collection_name(
    db: DbHandle
) -> List[ResourceName]:
    """Get all ResourceName."""
    try:
        # CRITICAL: Ensure database connection is ready
        if not db.resource_collection_name:
            try:
                db.init()
            except Exception as init_err:
                logger.error(f"Database not ready: {init_err}")
                # Return empty list if database isn't ready yet
                return []
        
        resource_collection_name = db.get_resource_collection_name()
        return [ResourceName(**emp) for emp in ResourceCollectionName]
    except Exception as e:
        logger.error(f"Failed to get resources: {e}")
        # Return empty list on error to keep frontend working
        return []
</code>
</connection_example>
</python_integration>
</instructions>
