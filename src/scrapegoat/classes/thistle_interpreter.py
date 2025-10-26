"""
"""

# IMPORTS
import re
from enum import Enum, auto
from .thistle import Thistle
from .conditions import InCondition, IfCondition


class TokenType(Enum):
    """
    """
    ACTION = auto()
    CONDITIONAL = auto()
    KEYWORD = auto()
    OPERATOR = auto()
    NUMBER = auto()
    IDENTIFIER = auto()
    NEGATION = auto()
    FLAG = auto()
    SEMICOLON = auto()
    UNKNOWN = auto()


class Token:
    """
    """
    def __init__(self, type: str, value: str):
        """
        """
        self.type = type
        self.value = value

    def __repr__(self):
        """
        """
        return f"Token(type={self.type}, value='{self.value}')"
    

class Tokenizer:
    def __init__(self):
        self.ACTIONS = {"select", "scrape"}
        self.CONDITIONALS = {"if", "in"}
        self.KEYWORDS = {"position"}
        self.OPERATORS = {"=", "!="}
        self.NEGATIONS = {"not"}
        self.FLAGS = {}

    def tokenize(self, query: str) -> list[Token]:
        """
        """
        tokens = []
        pattern = (r'(\bSELECT\b|\bSCRAPE\b|\bIN\b|\bIF\b|'r'!=|==|=|;|\n|'r'"(?:[^"]*)"|\'(?:[^\']*)\'|'r'@?[A-Za-z_][A-Za-z0-9_-]*|'r'\d+)')

        for match in re.finditer(pattern, query, flags=re.IGNORECASE):
            raw_value = match.group(0)
            token = self._classify_token(raw_value)
            tokens.append(token)
        return tokens

    def _classify_token(self, raw_value: str) -> Token:
        """
        """
        if raw_value[0] in ('"', "'") and raw_value[-1] == raw_value[0]:
            return Token(TokenType.IDENTIFIER, raw_value[1:-1])
        val_lower = raw_value.lower()
        if val_lower in self.ACTIONS:
            return Token(TokenType.ACTION, val_lower)
        if val_lower in self.CONDITIONALS:
            return Token(TokenType.CONDITIONAL, val_lower)
        if val_lower in self.KEYWORDS:
            return Token(TokenType.KEYWORD, val_lower)
        if val_lower in self.OPERATORS:
            return Token(TokenType.OPERATOR, val_lower)
        if val_lower in self.NEGATIONS:
            return Token(TokenType.NEGATION, val_lower)
        if raw_value == ";":
            return Token(TokenType.SEMICOLON, raw_value)
        if val_lower.isdigit():
            return Token(TokenType.NUMBER, val_lower)
        return Token(TokenType.IDENTIFIER, raw_value)
    

class ConditionParser:
    """
    """
    def __init__(self):
        """
        """
        pass

    def parse(self, tokens, index, element) -> tuple:
        negated = False
        if tokens[index].type == TokenType.NEGATION:
            negated = True
            index += 1
        token = tokens[index]
        if token.type != TokenType.CONDITIONAL:
            raise SyntaxError(f"Expected conditional at {token}")
        if token.value == "if":
            return self._parse_if(tokens, index, element, negated)
        elif token.value == "in":
            return self._parse_in(tokens, index, element, negated)
        
    def _parse_if(self, tokens, index, element, negated) -> tuple:
        """
        """
        index += 1
        token = tokens[index]
        if token.type != TokenType.IDENTIFIER:
            raise SyntaxError(f"Expected key after IF at {token}")
        key = token.value
        index += 1
        token = tokens[index]
        if token.type != TokenType.OPERATOR:
            raise SyntaxError(f"Expected '=' after IF {key} at {token}")
        if token.value == "!=":
            negated = True
        index += 1
        token = tokens[index]
        if token.type not in {TokenType.IDENTIFIER, TokenType.NUMBER}:
            raise SyntaxError(f"Expected value after IF {key} = at {token}")
        value = token.value
        condition = IfCondition(key=key, value=value, negated=negated, query_tag=element)
        index += 1
        return condition, index
    
    def _parse_in(self, tokens, index, element, negated) -> tuple:
        """
        """
        index += 1
        token = tokens[index]
        if token.type == TokenType.KEYWORD:
            index += 1
            token = tokens[index]
            if token.type != TokenType.OPERATOR:
                raise SyntaxError(f"Expected '=' after IN POSITION at {token}")
            if token.value == "!=":
                negated = True
            index += 1
            token = tokens[index]
            if token.type != TokenType.NUMBER:
                raise SyntaxError(f"Expected number after IN POSITION = at {token}")
            position = int(token.value)
            condition = InCondition(target="POSITION", value=position, negated=negated, query_tag=element)
        else:
            if token.type != TokenType.IDENTIFIER:
                raise SyntaxError(f"Expected element after IN at {token}")
            target = token.value
            condition = InCondition(target=target, negated=negated, query_tag=element)
        index += 1
        return condition, index


class ThistleInterpreter:
    """
    """
    def __init__(self):
        self.tokenizer = Tokenizer()
        self.condition_parser = ConditionParser()

    def interpret(self, query: str) -> list[Thistle]:
        tokens = self.tokenizer.tokenize(query)
        instructions = []
        index = 0
        while index < len(tokens):
            action, index = self._parse_action(tokens, index)
            count, index = self._parse_count(tokens, index)
            element, index = self._parse_element(tokens, index)
            
            conditions = []
            while tokens[index].type != TokenType.SEMICOLON:
                condition, index = self.condition_parser.parse(tokens, index, element)
                conditions.append(condition)

            instructions.append(Thistle(action=action, count=count, element=element, conditions=conditions))
            index += 1
        return instructions
        
    def _parse_action(self, tokens, index) -> tuple:
        """
        """
        token = tokens[index]
        if token.type != TokenType.ACTION:
            raise SyntaxError(f"Expected SCRAPE or SELECT at token {token}")
        action = token.value
        index += 1
        return action, index

    def _parse_count(self, tokens, index) -> tuple:
        """
        """
        token = tokens[index]
        if token.type != TokenType.NUMBER:
            count = 0
        else:
            count = int(token.value)
            index += 1
        return count, index

    def _parse_element(self, tokens, index) -> tuple:
        """
        """
        token = tokens[index]
        if token.type != TokenType.IDENTIFIER:
            raise SyntaxError(f"Expected element at token {token}")
        element = token.value
        index += 1
        return element, index
    
            
def main():
    """
    """
    pass


if __name__ == "__main__":
    main()
