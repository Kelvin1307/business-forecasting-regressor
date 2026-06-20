from pydantic import BaseModel, Field


class BudgetRequest(BaseModel):
    tv_budget: float = Field(..., ge=0, description="TV advertising budget")
    radio_budget: float = Field(..., ge=0, description="Radio advertising budget")
    digital_budget: float = Field(..., ge=0, description="Digital advertising budget")
