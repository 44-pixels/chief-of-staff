#!/usr/bin/env python3
"""
Chief of Staff - Daily Cron Integration
Runs at 8 PM daily to prepare for next day's meetings
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from orchestrator import ChiefOfStaffOrchestrator
import asyncio
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def main():
    """Main entry point for cron job"""
    try:
        orchestrator = ChiefOfStaffOrchestrator()
        await orchestrator.run_daily_prep()
    except Exception as e:
        logging.error(f"Chief of Staff cron job failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
