from setuptools import setup, find_packages

setup(
    name="todo-backend",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.115.0",
        "sqlmodel>=0.0.22",
        "uvicorn[standard]==0.32.0",
        "python-jose[cryptography]==3.3.0",
        "python-dotenv==1.0.0",
        "pydantic==2.12.5",
        "pydantic-settings==2.1.0",
        "passlib[bcrypt]==1.7.4",
        "cohere==5.12.0",
        "slowapi==0.1.9",
    ],
    python_requires=">=3.7",
)