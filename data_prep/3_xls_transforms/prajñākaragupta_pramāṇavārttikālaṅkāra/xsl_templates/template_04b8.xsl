<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" encoding="UTF-8">
<xsl:output method="xml" indent="yes"/>
<xsl:strip-space elements="*" />

<xsl:template match="@*|node()">
<xsl:copy>
<xsl:apply-templates select="@*|node()"/>
</xsl:copy>
</xsl:template>

<xsl:template match="div[parent::body and not(@label)]">
<xsl:copy>

<xsl:attribute name="label">
<xsl:value-of select="@n"/>
</xsl:attribute>
<xsl:apply-templates select="@*|node()" />

</xsl:copy>
</xsl:template>


<xsl:template match="div[not(parent::body) and not(@label) and parent::div[@label]]">
<xsl:copy>

<xsl:attribute name="label">
<xsl:value-of select="concat(parent::div/@label, '.', self::div/@n)"/>
</xsl:attribute>
<xsl:apply-templates select="@*|node()" />

</xsl:copy>
</xsl:template>

</xsl:stylesheet>
