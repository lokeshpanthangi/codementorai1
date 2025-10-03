"""
MongoDB Collection Schemas Documentation
=========================================

This file documents the structure of all MongoDB collections used in CodeMentor AI.
Each schema includes field descriptions, data types, indexes, and relationships.

Collections:
1. users - User accounts and statistics
2. problems - Coding problems catalog
3. testcases - Test cases for problems
4. submissions - User code submissions
5. categories - Problem categories/topics
6. aichathistory - AI chat interactions
7. userprogress - Per-problem user progress
8. dailychallenges - Daily challenge problems
"""

# ============================================================================
# 1. USERS COLLECTION
# ============================================================================
USERS_SCHEMA = {
    "_id": "ObjectId",  # Primary key
    "username": "str (unique, 3-50 chars)",
    "email": "str (unique, valid email)",
    "password_hash": "str (bcrypt hashed)",
    "full_name": "str (optional)",
    "avatar_url": "str (optional, default: placeholder)",
    "role": "str (user/admin/premium, default: user)",
    
    "subscription": {
        "type": "str (free/premium/enterprise, default: free)",
        "started_at": "datetime",
        "expires_at": "datetime (optional)"
    },
    
    "stats": {
        "total_solved": "int (default: 0)",
        "easy_solved": "int (default: 0)",
        "medium_solved": "int (default: 0)",
        "hard_solved": "int (default: 0)",
        "total_submissions": "int (default: 0)",
        "acceptance_rate": "float (default: 0.0)",
        "current_streak": "int (default: 0)",
        "longest_streak": "int (default: 0)",
        "reputation_points": "int (default: 0)"
    },
    
    "preferences": {
        "default_language": "str (default: python3)",
        "theme": "str (dark/light, default: dark)",
        "editor_font_size": "int (default: 14)",
        "ai_hints_enabled": "bool (default: true)"
    },
    
    "created_at": "datetime",
    "updated_at": "datetime",
    "last_login": "datetime"
}

USERS_INDEXES = [
    {"field": "email", "unique": True},
    {"field": "username", "unique": True},
    {"field": "stats.total_solved", "type": "descending"}
]

# ============================================================================
# 2. PROBLEMS COLLECTION
# ============================================================================
PROBLEMS_SCHEMA = {
    "_id": "ObjectId",
    "problem_number": "int (unique, sequential)",
    "title": "str",
    "slug": "str (unique, URL-friendly)",
    "difficulty": "str (Easy/Medium/Hard)",
    "category": "str (primary category)",
    "topics": ["str"] ,  # Array of topic tags
    "companies": ["str"],  # Companies that ask this
    
    "description": {
        "problem_statement": "str (markdown)",
        "examples": [
            {
                "input": "str",
                "output": "str",
                "explanation": "str (optional)"
            }
        ],
        "constraints": ["str"]
    },
    
    "hints": ["str"],  # Progressive hints
    
    "solution_templates": {
        "python3": "str (starter code)",
        "javascript": "str",
        "java": "str",
        "cpp": "str",
        "c": "str",
        "csharp": "str",
        "go": "str",
        "rust": "str",
        "kotlin": "str",
        "swift": "str",
        "php": "str",
        "ruby": "str",
        "typescript": "str"
    },
    
    "starter_code": {
        "python3": {
            "function_name": "str",
            "parameters": ["str"],
            "return_type": "str"
        }
        # Similar for other languages
    },
    
    "stats": {
        "total_submissions": "int (default: 0)",
        "total_accepted": "int (default: 0)",
        "acceptance_rate": "float (default: 0.0)",
        "difficulty_rating": "float (1-5, default: 3.0)",
        "total_solved": "int (default: 0)",
        "like_count": "int (default: 0)",
        "dislike_count": "int (default: 0)"
    },
    
    "frequency": {
        "last_6_months": "int (0-100, default: 50)",
        "trend": "str (increasing/stable/decreasing)"
    },
    
    "premium_only": "bool (default: false)",
    "is_daily_challenge": "bool (default: false)",
    "time_complexity": "str (Big-O notation)",
    "space_complexity": "str (Big-O notation)",
    "similar_problems": ["int"],  # Problem numbers
    
    "created_at": "datetime",
    "updated_at": "datetime"
}

PROBLEMS_INDEXES = [
    {"field": "problem_number", "unique": True},
    {"field": "slug", "unique": True},
    {"field": "difficulty"},
    {"field": "topics", "type": "multikey"},
    {"field": "companies", "type": "multikey"},
    {"field": "stats.acceptance_rate", "type": "descending"},
    {"field": "frequency.last_6_months", "type": "descending"}
]

# ============================================================================
# 3. TESTCASES COLLECTION
# ============================================================================
TESTCASES_SCHEMA = {
    "_id": "ObjectId",
    "problem_id": "ObjectId (ref: problems._id)",
    "problem_number": "int (denormalized for quick lookup)",
    "test_case_number": "int (1-based ordering)",
    "is_hidden": "bool (false=visible Run, true=hidden Submit)",
    "is_sample": "bool (true if shown in problem description)",
    
    "input_data": "dict (structured input)",
    "input_string": "str (formatted for display)",
    "expected_output": "any (structured output)",
    "expected_output_string": "str (formatted for display)",
    "explanation": "str (optional)",
    
    "test_type": "str (basic/edge_case/performance/corner_case)",
    "difficulty": "str (easy/medium/hard)",
    "time_limit_ms": "int (default: 2000)",
    "memory_limit_mb": "int (default: 256)",
    
    "created_at": "datetime"
}

TESTCASES_INDEXES = [
    {"field": "problem_id"},
    {"field": "problem_number"},
    {"field": "is_hidden"},
    {"field": "is_sample"},
    {"field": ["problem_id", "test_case_number"], "type": "compound"}
]

# Test Case Distribution Guidelines:
# - Visible (is_hidden: false): 3 test cases (for Run button)
# - Hidden (is_hidden: true): 5-10 test cases (for Submit button)
# - Sample (is_sample: true): 1-2 test cases (shown in description)

# ============================================================================
# 4. SUBMISSIONS COLLECTION
# ============================================================================
SUBMISSIONS_SCHEMA = {
    "_id": "ObjectId",
    "user_id": "ObjectId (ref: users._id)",
    "problem_id": "ObjectId (ref: problems._id)",
    "problem_number": "int (denormalized)",
    
    "language": "str (python3/javascript/java/etc)",
    "code": "str (source code)",
    "submission_type": "str (run/submit)",
    
    "status": "str (Accepted/Wrong Answer/TLE/etc)",
    "test_results": [
        {
            "test_case_id": "ObjectId",
            "test_case_number": "int",
            "status": "str",
            "passed": "bool",
            "runtime_ms": "int",
            "memory_kb": "int",
            "stdout": "str",
            "stderr": "str",
            "compile_output": "str",
            "expected_output": "str",
            "user_output": "str"
        }
    ],
    
    "summary": {
        "total_tests": "int",
        "passed_tests": "int",
        "failed_tests": "int",
        "avg_runtime_ms": "float",
        "avg_memory_kb": "float",
        "time_percentile": "float (0-100)",
        "memory_percentile": "float (0-100)"
    },
    
    "score": "int (0-100)",
    "runtime_ms": "int (best case)",
    "memory_kb": "int (peak memory)",
    "submitted_at": "datetime",
    "execution_time_ms": "int (total for all tests)",
    "is_accepted": "bool",
    "error_message": "str (optional)"
}

SUBMISSIONS_INDEXES = [
    {"field": "user_id"},
    {"field": "problem_id"},
    {"field": "status"},
    {"field": "submitted_at", "type": "descending"},
    {"field": ["user_id", "problem_id"], "type": "compound"},
    {"field": ["user_id", "submitted_at"], "type": "compound"}
]

# ============================================================================
# 5. CATEGORIES COLLECTION
# ============================================================================
CATEGORIES_SCHEMA = {
    "_id": "ObjectId",
    "name": "str (Array, String, Tree, etc)",
    "slug": "str (unique, URL-friendly)",
    "description": "str",
    "icon": "str (emoji)",
    "color": "str (hex color)",
    
    "problem_count": "int (default: 0)",
    "difficulty_distribution": {
        "easy": "int (default: 0)",
        "medium": "int (default: 0)",
        "hard": "int (default: 0)"
    },
    
    "parent_category": "ObjectId (optional, for subcategories)",
    "order": "int (display order)",
    "is_active": "bool (default: true)"
}

CATEGORIES_INDEXES = [
    {"field": "slug", "unique": True},
    {"field": "order"}
]

# ============================================================================
# 6. AICHATHISTORY COLLECTION
# ============================================================================
AICHATHISTORY_SCHEMA = {
    "_id": "ObjectId",
    "user_id": "ObjectId (ref: users._id)",
    "problem_id": "ObjectId (ref: problems._id)",
    "session_id": "str (UUID)",
    "chat_type": "str (insights/voice/chat)",
    
    "messages": [
        {
            "role": "str (user/assistant)",
            "content": "str",
            "timestamp": "datetime"
        }
    ],
    
    "code_snapshot": "str (code when chat started)",
    "language": "str",
    
    "insights_generated": [
        {
            "text": "str",
            "timestamp": "datetime"
        }
    ],
    
    "created_at": "datetime",
    "updated_at": "datetime"
}

AICHATHISTORY_INDEXES = [
    {"field": ["user_id", "problem_id"], "type": "compound"},
    {"field": "session_id"},
    {"field": "created_at", "type": "descending"}
]

# ============================================================================
# 7. USERPROGRESS COLLECTION
# ============================================================================
USERPROGRESS_SCHEMA = {
    "_id": "ObjectId",
    "user_id": "ObjectId (ref: users._id)",
    "problem_id": "ObjectId (ref: problems._id)",
    "problem_number": "int (denormalized)",
    
    "status": "str (attempted/solved/todo)",
    
    "first_attempt_at": "datetime",
    "last_attempt_at": "datetime",
    "solved_at": "datetime (optional)",
    "attempts_count": "int (default: 0)",
    
    "languages_used": ["str"],
    
    "best_submission": {
        "submission_id": "ObjectId",
        "runtime_ms": "int",
        "memory_kb": "int",
        "submitted_at": "datetime"
    },
    
    "hints_used": "int (default: 0)",
    "time_spent_seconds": "int (default: 0)",
    "notes": "str (optional, user notes)",
    "is_favorite": "bool (default: false)",
    "difficulty_rating": "int (1-5, user's own rating)",
    "tags": ["str (revisit/important/etc)"]
}

USERPROGRESS_INDEXES = [
    {"field": ["user_id", "problem_id"], "type": "compound", "unique": True},
    {"field": ["user_id", "status"], "type": "compound"},
    {"field": "solved_at", "type": "descending"}
]

# ============================================================================
# 8. DAILYCHALLENGES COLLECTION
# ============================================================================
DAILYCHALLENGES_SCHEMA = {
    "_id": "ObjectId",
    "date": "datetime (date only, unique)",
    "problem_id": "ObjectId (ref: problems._id)",
    "problem_number": "int (denormalized)",
    
    "bonus_points": "int (default: 50)",
    "participants_count": "int (default: 0)",
    "solvers_count": "int (default: 0)",
    "average_time_minutes": "float (default: 0.0)",
    
    "created_at": "datetime"
}

DAILYCHALLENGES_INDEXES = [
    {"field": "date", "unique": True},
    {"field": "date", "type": "descending"}
]

# ============================================================================
# RELATIONSHIPS
# ============================================================================
RELATIONSHIPS = """
1. users -> userprogress (one-to-many)
2. users -> submissions (one-to-many)
3. users -> aichathistory (one-to-many)
4. problems -> testcases (one-to-many)
5. problems -> submissions (one-to-many)
6. problems -> userprogress (one-to-many)
7. problems -> aichathistory (one-to-many)
8. categories -> problems (one-to-many, via category field)
9. dailychallenges -> problems (many-to-one)
"""

# ============================================================================
# DATA VALIDATION RULES
# ============================================================================
VALIDATION_RULES = {
    "username": "3-50 chars, alphanumeric + underscore",
    "email": "Valid email format",
    "password": "Min 6 chars (before hashing)",
    "difficulty": "Enum: Easy, Medium, Hard",
    "language": "One of: python3, javascript, typescript, java, cpp, c, csharp, go, rust, kotlin, swift, php, ruby",
    "submission_status": "Accepted, Wrong Answer, Time Limit Exceeded, Memory Limit Exceeded, Runtime Error, Compilation Error",
    "role": "Enum: user, admin, premium",
    "subscription_type": "Enum: free, premium, enterprise",
    "theme": "Enum: dark, light"
}
