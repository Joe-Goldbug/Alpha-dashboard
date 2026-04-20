import sys
import asyncio
sys.path.insert(0, '/workspace/WQOS')
from src.lib.simulation.core.session_manager import UnifiedSessionManager

async def main():
    manager = UnifiedSessionManager()
    await manager.initialize()
    
    alpha_id = "blWbAK8K"
    resp = await manager.get_json(f"https://api.worldquantbrain.com/alphas/{alpha_id}")
    if resp:
        print("--- Alpha Details ---")
        print(f"ID: {resp.get('id')}")
        print(f"Expression: {resp.get('regular', resp.get('regular_expression', 'N/A'))}")
        settings = resp.get('settings', {})
        print(f"Region: {settings.get('region')}")
        print(f"Universe: {settings.get('universe')}")
        print(f"Delay: {settings.get('delay')}")
        print(f"Neutralization: {settings.get('neutralization')}")
        print(f"Decay: {settings.get('decay')}")
        
        is_stats = resp.get('is', {})
        print("--- Metrics ---")
        print(f"Sharpe: {is_stats.get('sharpe')}")
        print(f"Fitness: {is_stats.get('fitness')}")
        print(f"Turnover: {is_stats.get('turnover')}")
        print(f"Margin: {is_stats.get('margin')}")
        
        # Check submission status
        check_url = f"https://api.worldquantbrain.com/alphas/{alpha_id}/check"
        check_resp = await manager.get_json(check_url)
        print("--- Submission Checks ---")
        if check_resp:
            checks = check_resp.get('checks', [])
            for c in checks:
                print(f"Check {c.get('name')}: {c.get('result')} - {c.get('details', '')}")
        else:
            print("No check response.")
    else:
        print(f"Failed to get alpha details for {alpha_id}")
    
    await manager.close()

if __name__ == '__main__':
    asyncio.run(main())
