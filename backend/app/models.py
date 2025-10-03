from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional, List, Any, Dict
from datetime import datetime
from bson import ObjectId
from pydantic_core import core_schema
from enum import Enum

# Custom ObjectId type for Pydantic v2
class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: Any, handler):
        return core_schema.union_schema(
            [
                core_schema.is_instance_schema(ObjectId),
                core_schema.chain_schema(
                    [
                        core_schema.str_schema(),
                        core_schema.no_info_plain_validator_function(cls.validate),
                    ]
                ),
            ],
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: str(x)
            ),
        )

    @classmethod
    def validate(cls, v):
        if isinstance(v, ObjectId):
            return v
        if isinstance(v, str) and ObjectId.is_valid(v):
            return ObjectId(v)
        raise ValueError("Invalid ObjectId")

# ============= ENUMS =============
class DifficultyEnum(str, Enum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"

class LanguageEnum(str, Enum):
    PYTHON3 = "python3"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    JAVA = "java"
    CPP = "cpp"
    C = "c"
    CSHARP = "csharp"
    GO = "go"
    RUST = "rust"
    KOTLIN = "kotlin"
    SWIFT = "swift"
    PHP = "php"
    RUBY = "ruby"

class SubmissionStatusEnum(str, Enum):
    ACCEPTED = "Accepted"
    WRONG_ANSWER = "Wrong Answer"
    TIME_LIMIT_EXCEEDED = "Time Limit Exceeded"
    MEMORY_LIMIT_EXCEEDED = "Memory Limit Exceeded"
    RUNTIME_ERROR = "Runtime Error"
    COMPILATION_ERROR = "Compilation Error"
    INTERNAL_ERROR = "Internal Error"

class UserRoleEnum(str, Enum):
    USER = "user"
    ADMIN = "admin"
    PREMIUM = "premium"

class SubscriptionTypeEnum(str, Enum):
    FREE = "free"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"

class ProgressStatusEnum(str, Enum):
    TODO = "todo"
    ATTEMPTED = "attempted"
    SOLVED = "solved"

# ============= USER MODELS =============
class SubscriptionInfo(BaseModel):
    type: SubscriptionTypeEnum = SubscriptionTypeEnum.FREE
    started_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None

class UserStats(BaseModel):
    total_solved: int = 0
    easy_solved: int = 0
    medium_solved: int = 0
    hard_solved: int = 0
    total_submissions: int = 0
    acceptance_rate: float = 0.0
    current_streak: int = 0
    longest_streak: int = 0
    reputation_points: int = 0

class UserPreferences(BaseModel):
    default_language: LanguageEnum = LanguageEnum.PYTHON3
    theme: str = "dark"
    editor_font_size: int = 14
    ai_hints_enabled: bool = True

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserInDB(UserBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    hashed_password: str
    avatar_url: str = "https://api.dicebear.com/7.x/avataaars/svg?seed=default"
    role: UserRoleEnum = UserRoleEnum.USER
    subscription: SubscriptionInfo = Field(default_factory=SubscriptionInfo)
    stats: UserStats = Field(default_factory=UserStats)
    preferences: UserPreferences = Field(default_factory=UserPreferences)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class UserResponse(UserBase):
    id: str
    avatar_url: str
    role: str
    stats: UserStats
    created_at: datetime
    
    class Config:
        from_attributes = True

# ============= PROBLEM MODELS =============
class ProblemExample(BaseModel):
    input: str
    output: str
    explanation: Optional[str] = None

class ProblemDescription(BaseModel):
    problem_statement: str
    examples: List[ProblemExample]
    constraints: List[str]

class ProblemStats(BaseModel):
    total_submissions: int = 0
    total_accepted: int = 0
    acceptance_rate: float = 0.0
    difficulty_rating: float = 3.0
    total_solved: int = 0
    like_count: int = 0
    dislike_count: int = 0

class ProblemFrequency(BaseModel):
    last_6_months: int = 50
    trend: str = "stable"

class ProblemBase(BaseModel):
    title: str
    slug: str  # URL-friendly: "two-sum"
    difficulty: DifficultyEnum
    category: str = "General"
    topics: List[str] = []
    companies: List[str] = []

class ProblemCreate(ProblemBase):
    description: ProblemDescription
    hints: List[str] = []
    solution_templates: Dict[str, str] = {}

class ProblemInDB(ProblemBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    problem_number: int
    description: ProblemDescription
    hints: List[str] = []
    solution_templates: Dict[str, str] = {}
    starter_code: Dict[str, Dict] = {}
    stats: ProblemStats = Field(default_factory=ProblemStats)
    frequency: ProblemFrequency = Field(default_factory=ProblemFrequency)
    premium_only: bool = False
    is_daily_challenge: bool = False
    time_complexity: Optional[str] = None
    space_complexity: Optional[str] = None
    similar_problems: List[int] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class ProblemResponse(BaseModel):
    id: str
    problem_number: int
    title: str
    slug: str
    difficulty: str
    category: str
    topics: List[str]
    companies: List[str]
    acceptance_rate: float
    frequency: int
    
    class Config:
        from_attributes = True

class ProblemDetail(ProblemResponse):
    description: ProblemDescription
    hints: List[str]
    solution_templates: Dict[str, str]
    stats: ProblemStats
    time_complexity: Optional[str]
    space_complexity: Optional[str]
    similar_problems: List[int]

# ============= TEST CASE MODELS =============
class TestCaseBase(BaseModel):
    problem_id: str
    problem_number: int
    test_case_number: int
    is_hidden: bool  # False = visible (Run), True = hidden (Submit)
    is_sample: bool = False  # True if shown in problem description

class TestCaseCreate(TestCaseBase):
    input_data: Dict[str, Any]
    input_string: str
    expected_output: Any
    expected_output_string: str
    explanation: Optional[str] = None
    test_type: str = "basic"
    difficulty: str = "easy"

class TestCaseInDB(TestCaseBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    input_data: Dict[str, Any]
    input_string: str
    expected_output: Any
    expected_output_string: str
    explanation: Optional[str] = None
    test_type: str = "basic"
    difficulty: str = "easy"
    time_limit_ms: int = 2000
    memory_limit_mb: int = 256
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class TestCaseResponse(BaseModel):
    id: str
    test_case_number: int
    is_hidden: bool
    input_string: str
    expected_output_string: str
    explanation: Optional[str]
    
    class Config:
        from_attributes = True

# ============= SUBMISSION MODELS =============
class TestResult(BaseModel):
    test_case_id: str
    test_case_number: int
    status: str
    passed: bool
    runtime_ms: int
    memory_kb: int
    stdout: str = ""
    stderr: str = ""
    compile_output: str = ""
    expected_output: str
    user_output: str

class SubmissionSummary(BaseModel):
    total_tests: int
    passed_tests: int
    failed_tests: int
    avg_runtime_ms: float = 0.0
    avg_memory_kb: float = 0.0
    time_percentile: float = 0.0
    memory_percentile: float = 0.0

class SubmissionBase(BaseModel):
    user_id: str
    problem_id: str
    problem_number: int
    language: LanguageEnum
    code: str
    submission_type: str = "submit"  # "run" or "submit"

class SubmissionCreate(SubmissionBase):
    pass

class SubmissionInDB(SubmissionBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    status: SubmissionStatusEnum
    test_results: List[TestResult] = []
    summary: Optional[SubmissionSummary] = None
    score: int = 0
    runtime_ms: int = 0
    memory_kb: int = 0
    submitted_at: datetime = Field(default_factory=datetime.utcnow)
    execution_time_ms: int = 0
    is_accepted: bool = False
    error_message: Optional[str] = None
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class SubmissionResponse(BaseModel):
    id: str
    status: str
    score: int
    test_results: List[TestResult]
    summary: Optional[SubmissionSummary]
    submitted_at: datetime
    
    class Config:
        from_attributes = True

# ============= USER PROGRESS MODELS =============
class BestSubmission(BaseModel):
    submission_id: str
    runtime_ms: int
    memory_kb: int
    submitted_at: datetime

class UserProgressBase(BaseModel):
    user_id: str
    problem_id: str
    problem_number: int
    status: ProgressStatusEnum = ProgressStatusEnum.TODO

class UserProgressCreate(UserProgressBase):
    pass
    
class UserProgressInDB(UserProgressBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    first_attempt_at: Optional[datetime] = None
    last_attempt_at: Optional[datetime] = None
    solved_at: Optional[datetime] = None
    attempts_count: int = 0
    languages_used: List[str] = []
    best_submission: Optional[BestSubmission] = None
    hints_used: int = 0
    time_spent_seconds: int = 0
    notes: str = ""
    is_favorite: bool = False
    difficulty_rating: Optional[int] = None
    tags: List[str] = []
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class UserProgressResponse(BaseModel):
    id: str
    problem_number: int
    status: str
    attempts_count: int
    solved_at: Optional[datetime]
    
    class Config:
        from_attributes = True

# ============= CATEGORY MODELS =============
class DifficultyDistribution(BaseModel):
    easy: int = 0
    medium: int = 0
    hard: int = 0

class CategoryBase(BaseModel):
    name: str
    slug: str
    description: str = ""
    icon: str = "📁"
    color: str = "#3b82f6"

class CategoryCreate(CategoryBase):
    pass

class CategoryInDB(CategoryBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    problem_count: int = 0
    difficulty_distribution: DifficultyDistribution = Field(default_factory=DifficultyDistribution)
    parent_category: Optional[str] = None
    order: int = 0
    is_active: bool = True
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class CategoryResponse(BaseModel):
    id: str
    name: str
    slug: str
    icon: str
    color: str
    problem_count: int
    difficulty_distribution: DifficultyDistribution
    
    class Config:
        from_attributes = True

# ============= AI CHAT HISTORY MODELS =============
class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class AIInsight(BaseModel):
    text: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class AIChatHistoryBase(BaseModel):
    user_id: str
    problem_id: str
    session_id: str
    chat_type: str = "insights"  # insights/voice/chat

class AIChatHistoryCreate(AIChatHistoryBase):
    code_snapshot: str = ""
    language: LanguageEnum = LanguageEnum.PYTHON3

class AIChatHistoryInDB(AIChatHistoryBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    messages: List[ChatMessage] = []
    code_snapshot: str = ""
    language: str = "python3"
    insights_generated: List[AIInsight] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

# ============= DAILY CHALLENGE MODELS =============
class DailyChallengeBase(BaseModel):
    date: datetime
    problem_id: str
    problem_number: int

class DailyChallengeCreate(DailyChallengeBase):
    pass

class DailyChallengeInDB(DailyChallengeBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    bonus_points: int = 50
    participants_count: int = 0
    solvers_count: int = 0
    average_time_minutes: float = 0.0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class DailyChallengeResponse(BaseModel):
    id: str
    date: datetime
    problem_number: int
    bonus_points: int
    participants_count: int
    
    class Config:
        from_attributes = True

# ============= AUTH MODELS =============
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
