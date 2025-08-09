import json
import os
from src.agents import OrchestratorAgent

def load_topics():
    """Load topics from topics.json file"""
    try:
        with open('topics.json', 'r') as f:
            data = json.load(f)
            return data.get('topics', [])
    except FileNotFoundError:
        print("Error: topics.json not found")
        return []

def update_topic_status(topic_id, status):
    """Update topic status in topics.json"""
    try:
        with open('topics.json', 'r') as f:
            data = json.load(f)
        
        for topic in data['topics']:
            if topic['id'] == topic_id:
                topic['status'] = status
                if status == 'completed':
                    from datetime import datetime
                    topic['completed_at'] = datetime.now().isoformat()[:10]
                break
        
        with open('topics.json', 'w') as f:
            json.dump(data, f, indent=2)
        
        return True
    except Exception as e:
        print(f"Error updating topic status: {e}")
        return False

def process_next_topic():
    """Process the next topic with status 'new'"""
    topics = load_topics()
    new_topics = [t for t in topics if t['status'] == 'new']
    
    if not new_topics:
        print("No new topics to process")
        return
    
    topic = new_topics[0]
    topic_id = topic['id']
    topic_title = topic['title']
    
    print(f"Processing topic: {topic_title} ({topic_id})")
    
    # Update status to in_progress
    update_topic_status(topic_id, 'in_progress')
    
    # Create topic-specific directory
    topic_dir = f"artifacts/{topic_id}"
    os.makedirs(topic_dir, exist_ok=True)
    
    # Process the topic
    orchestrator = OrchestratorAgent()
    narrative = orchestrator.execute(topic_title)
    
    # Update status to completed
    update_topic_status(topic_id, 'completed')
    
    print(f"\n✅ Completed processing: {topic_title}")
    print(f"📁 Artifacts saved to: {topic_dir}")

def main():
    process_next_topic()

if __name__ == "__main__":
    main()