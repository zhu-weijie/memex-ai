# src/memex_ai/tools/memory.py
from langmem import create_manage_memory_tool, create_search_memory_tool
from langmem.store import Memory

_memory = Memory()

manage_memory = create_manage_memory_tool(_memory)
search_memory = create_search_memory_tool(_memory)
