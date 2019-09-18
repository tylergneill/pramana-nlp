<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" encoding="UTF-8">
<xsl:output method="xml" indent="yes"/>
<xsl:strip-space elements="*" />

<xsl:template match="@*|node()">
<xsl:copy>
<xsl:apply-templates select="@*|node()"/>
</xsl:copy>
</xsl:template>

<xsl:template match="//div">
<xsl:copy>

<xsl:attribute name="level">
<xsl:value-of select="count(ancestor::div)+1"/>
</xsl:attribute>

<xsl:attribute name="n">
<xsl:value-of select="count(preceding-sibling::div)+1"/>
</xsl:attribute>

<xsl:apply-templates select="@*|node()" />
</xsl:copy>
</xsl:template>

</xsl:stylesheet>
