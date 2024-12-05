from fastapi import FastAPI, HTTPException
from models.action import ActionRequest, ActionTrackRequest
from services.sequence_service import fetch_sequences_for_action, analyze_sequences, track_user_action

app = FastAPI(
    title="Action Sequence Predictor",
    description="API for tracking and predicting user action sequences",
    version="1.0.0"
)

@app.post("/predict_next_action")
async def predict_next_action(request: ActionRequest):
    if not request.current_action or not request.user_id:
        raise HTTPException(status_code=400, detail="Both current_action and user_id are required")
    
    # Fetch sequences from DB for specific user
    data = fetch_sequences_for_action(request.current_action, request.user_id)
    
    # Analyze and format the sequences
    result = analyze_sequences(data, request.current_action)
    
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
        
    # Print the sequences in a readable format
    print("\nAction Sequence Analysis:")
    print(f"User ID: {request.user_id}")
    print(f"Current Action: {result['current_action']}")
    print(f"Total Occurrences: {result['total_occurrences']}")
    print("\nPossible Next Actions:")
    print("-" * 50)
    print(f"{'Next Action':<20} {'Frequency':<10} {'Probability':<10}")
    print("-" * 50)
    
    for seq in result['sequences']:
        print(f"{seq['next_action']:<20} {seq['frequency']:<10} {seq['probability']}%")
    print("-" * 50)
    
    return result

@app.post("/track_action")
async def track_action(request: ActionTrackRequest):
    if not request.action_name or not request.user_id:
        raise HTTPException(status_code=400, detail="Both action_name and user_id are required")
    
    action_data = request.dict(exclude_unset=True)
    result = track_user_action(action_data)
    
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    # If tracking was successful, immediately return the updated predictions
    if result.get("status") == "success":
        prediction_result = await predict_next_action(
            ActionRequest(
                current_action=action_data["action_name"],
                user_id=action_data["user_id"]
            )
        )
        return {
            "tracking": result,
            "predictions": prediction_result
        }
    return result